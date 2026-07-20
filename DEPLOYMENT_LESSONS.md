# Deployment Lessons — RD School / RDPS Betul

Hard-won rules from real incidents on dev (`rdschool.localhost`), old prod
(168.144.155.237), and new prod (`rdps.trustbit.cloud`). Read this before any
deploy, app install, or new-server build.

**The one rule:** always deploy via `bash apps/rdschool/deploy.sh <site>` —
never hand-run `migrate`/`build` alone. The script pulls, migrates, builds,
reconciles roles/permissions, restarts, and refuses to pass unless
`verify_deployment()` prints HEALTHCHECK PASS.

---

## Lesson 1 — Fresh sites can silently miss ERPNext's install-time custom fields (2026-07-21)

**Incident:** On the fresh `rdps.trustbit.cloud` site, opening any RFQ (and the
same code path behind PO supplier-contact lookups) crashed with:

```
pymysql.err.OperationalError: (1054, "Unknown column 'tabContact.is_billing_contact' in 'WHERE'")
```

**Root cause:** ERPNext's `after_install` hook creates a handful of Custom
Fields (`Contact.is_billing_contact`, `Address.tax_category`,
`Address.is_your_company_address`, `Email Account.company`). On this site that
step silently didn't complete. Nothing notices until a form that queries those
columns is opened — weeks later.

**Why `bench migrate` does NOT fix it:** migrate only syncs schema for fields
that exist as DocField/Custom Field records. Here the Custom Field *records
themselves* were missing, so migrate had nothing to sync. (On the old dev box a
similar error WAS fixed by migrate — that was the other variant: record
present, column missing. Know which one you have: check
`Custom Field` list filtered by `dt = Contact`.)

**Fix (idempotent, safe to re-run any time):**

```bash
bench --site <site> execute erpnext.setup.install.create_print_setting_custom_fields
bench --site <site> execute erpnext.setup.install.create_address_and_contact_custom_fields
bench --site <site> execute erpnext.setup.install.create_custom_company_links
bench --site <site> clear-cache
```

**Rule for the future:**
- After bootstrapping ANY new site, run the three commands above once,
  then verify: `Contact.is_billing_contact` must exist as a column.
- If a user reports `Unknown column 'tabX.y'` anywhere: first check whether the
  Custom Field / DocField record exists. Record missing → re-run the app's
  install-time creator. Record present → `bench migrate`.
- TODO: add a `Contact.is_billing_contact` column check to
  `verify_deployment()` so the health gate catches this class of miss.

## Lesson 2 — Installing ANY app re-syncs role profiles and strips roles (2026-07-20)

Installing the `lms` app removed the `Employee` role from School users
(Frappe v15 `role_profile_name` sync wipes roles not in the profile).
**Rule:** after every `bench install-app <anything>`, run the deploy.sh
reconcile trio + health check:

```bash
bench --site <site> execute rdschool.setup_data.assign_full_profile_roles
bench --site <site> execute rdschool.setup_data.rebuild_school_docperms
bench --site <site> execute rdschool.setup_data.ensure_company_user_permissions
bench --site <site> execute rdschool.setup_data.verify_deployment   # must PASS
```

## Lesson 3 — A failed `bench get-app` leaves a half-registered app (2026-07-20)

If `get-app` dies mid-way (e.g. yarn failure), the app folder exists under
`apps/` but is NOT in `sites/apps.txt`. A later `bench build --app <app>` then
dies with `TypeError: paths[0] must be of type string` + exit 143 — which looks
like an OOM kill but isn't.
**Rule:** after any failed get-app, either finish the registration manually or
remove the folder before retrying. And never append to `apps.txt` with
`echo >>` — the file may lack a trailing newline (we corrupted it to
`erpnextlms` once). Rewrite the whole file or let bench manage it.

## Lesson 4 — Node version pins (2026-07-20)

Server Node was upgraded 18 → **20 LTS** (NodeSource) to build LMS. LMS is
**pinned at v2.53.0** (detached HEAD): every newer tag requires Node ≥ 22, and
`@iconify/utils` needs ≥ 20.12. **Rule:** do not update the lms app past
v2.53.0 without first moving the server to Node 22; Frappe v15 itself is fine
on Node 18/20.

## Lesson 5 — Fixtures bake the export-site's company into link_filters (2026-06-15)

`bench migrate` clobbers company-specific `link_filter`s with the dev company
name ("RD School Betul") on a prod site whose company is "RDPS Betul" → empty
dropdowns. Fixed by the `after_migrate` hook
(`relocalize_company_link_filters`), which auto-heals on every migrate.
**Rule:** never hardcode a company name anywhere (code, fixtures, JS); prod and
dev companies differ.

## Lesson 6 — One fixtures entry per doctype (2026-06-15)

Two `custom_field` fixture entries in hooks.py silently overwrite each other
(export writes one file per doctype; the second entry wins). We shipped 1/15
fields that way. **Rule:** exactly one fixtures entry per doctype; after any UI
field change run `bench export-fixtures --app rdschool` and eyeball the JSON
diff for lost rows.

## Lesson 7 — Custom-DocPerm roles need explicit READ on supporting masters (2026-06-15)

ERPNext buying/stock/accounts forms auto-load supporting masters (Address,
Contact, Terms, Price List, Warehouse, taxes, Mode of Payment…). School roles
use Custom DocPerms only, so any "No permission on <Master>" report from a
tester means: add the doctype to `SUPPORT_READ_DOCTYPES` in `setup_data.py` and
re-run `rebuild_school_docperms` on dev + prod.

## Lesson 8 — Misc server gotchas

- `certbot --nginx` (not `bench setup lets-encrypt`) issued the SSL cert on
  rdps.trustbit.cloud. Running `bench setup nginx` would drop SSL — re-run
  certbot if that ever happens. deploy.sh never touches nginx.
- Restart bench after every app install; a bench started before the install
  hits scheduler `ModuleNotFoundError`.
- Bench's redis must be running before `install-app` on a new box, or the
  install fails silently.
- `chmod 755 /home/frappe` or nginx can't serve assets; supervisor conf must be
  symlinked into `/etc/supervisor/conf.d/`.
