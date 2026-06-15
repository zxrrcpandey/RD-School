"""Seed data for the RD School Betul ERPNext site.

Run via:
    bench --site rdschool.localhost execute rdschool.setup_data.setup_all

Or run individual stages by their function name. Idempotent — safe to re-run.
"""

import frappe


def _company():
    """Resolve the active Company name at call time.

    Reading from Global Defaults instead of hard-coding lets this app survive
    being installed on a site whose company isn't literally 'RD School Betul'
    (the after_install hook then seeds whatever the wizard created).
    """
    name = frappe.defaults.get_global_default("company")
    if not name:
        raise RuntimeError(
            "No default Company set. Run the Setup Wizard before invoking rdschool seeds."
        )
    return name


def _abbr():
    return frappe.db.get_value("Company", _company(), "abbr")


def _demo_password():
    """Demo user password. Prefer site_config (rdschool_demo_password) over the
    hard-coded fallback. Set per site with:
        bench --site <site> set-config rdschool_demo_password 'mypass'
    """
    return frappe.conf.get("rdschool_demo_password") or "RdsDemo!2026"

DEPARTMENTS = [
    "Academic - Primary",
    "Academic - Secondary",
    "Academic - Senior Secondary",
    "Science Lab",
    "Computer Lab",
    "Library",
    "Sports & PE",
    "Administration",
    "Accounts & Finance",
    "Stores & Procurement",
    "Transport",
    "Maintenance & Housekeeping",
    "IT",
]

ROLE_PROFILES = {
    "School Teacher": [
        "Employee",
        "Stock User",
    ],
    "School HOD": [
        "Employee",
        "Stock User",
        "Purchase User",
    ],
    "School Principal": [
        "Employee",
        "Stock Manager",
        "Purchase Manager",
        "Accounts Manager",
    ],
    # Display intent: "Store / Purchase Manager". Role NAME kept as
    # "School Stores Incharge" because 24 live POs + fixtures link to it;
    # renaming the Role would break those. Profile upgraded to Purchase
    # Manager (was Purchase User) to cover PO release per the new SOP.
    "School Stores Incharge": [
        "Employee",
        "Stock Manager",
        "Purchase Manager",
        "Item Manager",
    ],
    "School Accountant": [
        "Employee",
        "Accounts User",
        "Purchase User",
    ],
    "School Auditor": [
        "Employee",
        "Auditor",
    ],
    # --- New roles for the multi-stage SOP (Phase A of the redesign) ---
    "School Vice Principal": [
        "Employee",
        "Stock User",
        "Purchase User",
    ],
    # Thin co-approver at the Principal gate (combined Principal+Director gate;
    # either may act). Optional person — harmless if unused.
    "School Director": [
        "Employee",
        "Purchase Manager",
    ],
    # G1 gate security: minimal desk access; scoped by DocPerm to Gate Entry.
    "School Gate Security": [
        "Employee",
    ],
    # Reception desk for the direct-inward route.
    "School Reception": [
        "Employee",
    ],
}

DEMO_USERS = [
    ("teacher1@rdschool.local", "Anita Teacher", "School Teacher", "Science Lab"),
    ("hod1@rdschool.local", "Harish HOD", "School HOD", "Science Lab"),
    ("vp@rdschool.local", "Vimala VicePrincipal", "School Vice Principal", "Administration"),
    ("principal@rdschool.local", "Ravi Principal", "School Principal", "Administration"),
    ("director@rdschool.local", "Deepak Director", "School Director", "Administration"),
    ("stores@rdschool.local", "Suresh Stores", "School Stores Incharge", "Stores & Procurement"),
    ("accountant@rdschool.local", "Priya Accounts", "School Accountant", "Accounts & Finance"),
    ("gate@rdschool.local", "Ganesh Gate", "School Gate Security", "Administration"),
    ("reception@rdschool.local", "Rekha Reception", "School Reception", "Administration"),
    ("auditor@rdschool.local", "Mohan Auditor", "School Auditor", "Accounts & Finance"),
]

# DEMO_USER_PASSWORD is resolved at seed time via _demo_password(). Override
# per site with `bench --site <site> set-config rdschool_demo_password '...'`.

SUPPLIER_GROUPS = [
    "School Stationery & Books",
    "Lab Supplies",
    "Sports & General",
]

SUPPLIERS = [
    # (name, supplier_group, country, default_currency)
    ("Sharma Stationers Betul", "School Stationery & Books", "India", "INR"),
    ("MP Lab Supplies Indore", "Lab Supplies", "India", "INR"),
    ("Apex Sports & General Store Bhopal", "Sports & General", "India", "INR"),
]

# Item Groups under the root "All Item Groups". Parent must already exist.
ITEM_GROUPS = [
    "School Stationery",
    "Textbooks & Library",
    "Lab Equipment",
    "Sports Equipment",
    "IT & Electronics",
    "Maintenance & Cleaning",
]

# Items: (item_code, item_name, item_group, uom, stock_uom, is_stock_item, standard_rate)
ITEMS = [
    ("RSB-STA-001", "A4 Paper Ream (500 sheets)", "School Stationery", "Nos", "Nos", 1, 280),
    ("RSB-STA-002", "Notebook 200 pages (Ruled)", "School Stationery", "Nos", "Nos", 1, 60),
    ("RSB-STA-003", "Whiteboard Marker - Black", "School Stationery", "Nos", "Nos", 1, 25),
    ("RSB-STA-004", "Chalk Box (100 pcs)", "School Stationery", "Box", "Box", 1, 80),
    ("RSB-LIB-001", "Mathematics Class 10 Textbook (NCERT)", "Textbooks & Library", "Nos", "Nos", 1, 195),
    ("RSB-LAB-001", "Glass Beaker 250ml", "Lab Equipment", "Nos", "Nos", 1, 75),
    ("RSB-LAB-002", "Bunsen Burner", "Lab Equipment", "Nos", "Nos", 1, 450),
    ("RSB-LAB-003", "pH Indicator Strips (Box of 100)", "Lab Equipment", "Box", "Box", 1, 220),
    ("RSB-SPT-001", "Football (Size 5)", "Sports Equipment", "Nos", "Nos", 1, 850),
    ("RSB-SPT-002", "Cricket Bat (Senior)", "Sports Equipment", "Nos", "Nos", 1, 1400),
    ("RSB-SPT-003", "Yoga Mat 6mm", "Sports Equipment", "Nos", "Nos", 1, 350),
    ("RSB-ITX-001", "HDMI Cable 2m", "IT & Electronics", "Nos", "Nos", 1, 220),
    ("RSB-ITX-002", "USB Pen Drive 32GB", "IT & Electronics", "Nos", "Nos", 1, 320),
    ("RSB-MTN-001", "Floor Cleaner 5L", "Maintenance & Cleaning", "Nos", "Nos", 1, 380),
    ("RSB-MTN-002", "LED Tube Light 18W", "Maintenance & Cleaning", "Nos", "Nos", 1, 240),
]


# Doctype perms granted to each School role. Format:
#   { role_name: [ (doctype, {perm_flag: 1, ...}), ... ] }
# Only flags set to 1 are persisted; everything unset stays at the default 0.
# These are ADDITIVE — applied only if no DocPerm row exists yet for
# (parent=doctype, role=role_name).
SCHOOL_ROLE_DOCPERMS = {
    "School Teacher": [
        ("Department", {"read": 1}),
        ("Cost Center", {"read": 1}),
        ("Item", {"read": 1}),
        ("Item Group", {"read": 1}),
        ("UOM", {"read": 1}),
        ("Supplier", {"read": 1}),
        ("Material Request", {
            "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1,
            "print": 1, "email": 1, "report": 1,
        }),
    ],
    "School HOD": [
        ("Department", {"read": 1}),
        ("Cost Center", {"read": 1}),
        ("Item", {"read": 1}),
        ("Item Group", {"read": 1}),
        ("UOM", {"read": 1}),
        ("Supplier", {"read": 1}),
        ("Material Request", {
            "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1,
            "print": 1, "email": 1, "report": 1,
        }),
    ],
    "School Principal": [
        ("Department", {"read": 1}),
        ("Cost Center", {"read": 1}),
        ("Item", {"read": 1}),
        ("Item Group", {"read": 1}),
        ("UOM", {"read": 1}),
        ("Supplier", {"read": 1}),
        ("Material Request", {
            "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1,
            "print": 1, "email": 1, "report": 1,
        }),
        ("Purchase Order", {"read": 1, "print": 1, "email": 1, "report": 1}),
        ("Purchase Receipt", {"read": 1, "print": 1, "email": 1, "report": 1}),
        ("Purchase Invoice", {"read": 1, "print": 1, "email": 1, "report": 1}),
    ],
    "School Stores Incharge": [
        ("Department", {"read": 1}),
        ("Cost Center", {"read": 1}),
        ("Item", {"read": 1, "write": 1, "create": 1}),
        ("Item Group", {"read": 1, "write": 1, "create": 1}),
        ("UOM", {"read": 1, "write": 1, "create": 1}),
        ("Supplier", {"read": 1, "write": 1, "create": 1}),
        # Write so Store can set rsb_stock_availability while the MR is in
        # Pending Store Verification (drives the T6/T7 branch).
        ("Material Request", {"read": 1, "write": 1, "print": 1, "report": 1}),
        ("Request for Quotation", {
            "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1,
            "print": 1, "email": 1, "report": 1,
        }),
        ("Supplier Quotation", {
            "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1,
            "print": 1, "email": 1, "report": 1,
        }),
        ("Purchase Order", {
            "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1,
            "print": 1, "email": 1, "report": 1,
        }),
        ("Purchase Receipt", {
            "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1,
            "print": 1, "email": 1, "report": 1,
        }),
    ],
    "School Accountant": [
        ("Department", {"read": 1}),
        ("Cost Center", {"read": 1}),
        ("Item", {"read": 1}),
        ("Supplier", {"read": 1, "write": 1, "create": 1}),
        ("Material Request", {"read": 1, "print": 1, "report": 1}),
        ("Purchase Order", {"read": 1, "print": 1, "report": 1}),
        ("Purchase Receipt", {"read": 1, "print": 1, "report": 1}),
        ("Purchase Invoice", {
            "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1,
            "print": 1, "email": 1, "report": 1,
        }),
        ("Payment Entry", {
            "read": 1, "write": 1, "create": 1, "submit": 1, "cancel": 1, "amend": 1,
            "print": 1, "email": 1, "report": 1,
        }),
    ],
    "School Auditor": [
        ("Department", {"read": 1}),
        ("Cost Center", {"read": 1}),
        ("Item", {"read": 1}),
        ("Supplier", {"read": 1}),
        ("Material Request", {"read": 1, "print": 1, "report": 1}),
        ("Request for Quotation", {"read": 1, "print": 1, "report": 1}),
        ("Supplier Quotation", {"read": 1, "print": 1, "report": 1}),
        ("Purchase Order", {"read": 1, "print": 1, "report": 1}),
        ("Purchase Receipt", {"read": 1, "print": 1, "report": 1}),
        ("Purchase Invoice", {"read": 1, "print": 1, "report": 1}),
        ("Payment Entry", {"read": 1, "print": 1, "report": 1}),
    ],
    # --- New roles (multi-stage SOP) ---
    "School Vice Principal": [
        ("Department", {"read": 1}),
        ("Cost Center", {"read": 1}),
        ("Item", {"read": 1}),
        ("Item Group", {"read": 1}),
        ("UOM", {"read": 1}),
        ("Supplier", {"read": 1}),
        # Read+write so the VP can act on workflow transitions and annotate;
        # no create/submit (VP reviews, does not raise or finalize).
        ("Material Request", {"read": 1, "write": 1, "print": 1, "report": 1}),
        ("Request for Quotation", {"read": 1, "report": 1}),
        ("Purchase Order", {"read": 1, "report": 1}),
    ],
    "School Director": [
        ("Department", {"read": 1}),
        ("Cost Center", {"read": 1}),
        ("Item", {"read": 1}),
        ("Supplier", {"read": 1}),
        # Co-approver at the Principal gate — same write access to act.
        ("Material Request", {"read": 1, "write": 1, "print": 1, "report": 1}),
        ("Request for Quotation", {"read": 1, "report": 1}),
        ("Supplier Quotation", {"read": 1, "report": 1}),
        ("Purchase Order", {"read": 1, "report": 1}),
    ],
    "School Gate Security": [
        # Gate doctype perms are added in Phase D. For now: read masters
        # needed to log arrivals (PO + Supplier), plus Department for context.
        ("Department", {"read": 1}),
        ("Supplier", {"read": 1}),
        ("Purchase Order", {"read": 1, "report": 1}),
    ],
    "School Reception": [
        ("Department", {"read": 1}),
        ("Supplier", {"read": 1}),
    ],
}


def _insert_company_user_permission(user, company):
    """Insert a User Permission row directly (the frappe.permissions
    add_user_permission helper signature varies across versions — direct
    insert is portable).
    """
    if frappe.db.exists(
        "User Permission",
        {"user": user, "allow": "Company", "for_value": company},
    ):
        return False
    frappe.get_doc(
        {
            "doctype": "User Permission",
            "user": user,
            "allow": "Company",
            "for_value": company,
            "apply_to_all_doctypes": 1,
            "is_default": 1,
        }
    ).insert(ignore_permissions=True)
    return True


def ensure_company_user_permissions():
    """Add a User Permission (Company = current company) for every System User
    that doesn't have one. Department and Cost Center enforce User Permissions
    by Company — without this row, a school-role-only user sees zero records
    in the dept/CC dropdowns even though the DocPerm grants read access.

    Idempotent. Skips Administrator (bypasses User Permissions anyway) and
    Guest. Run any time; safe to re-run.
    """
    company = _company()
    affected = 0
    for email in frappe.db.sql_list(
        "select name from tabUser where user_type = 'System User' "
        "and name not in ('Administrator', 'Guest') and enabled = 1"
    ):
        if _insert_company_user_permission(email, company):
            affected += 1
    frappe.clear_cache()
    print(f"ensure_company_user_permissions: added UP for {affected} users -> {company}")


def auto_add_company_user_permission(doc, method=None):
    """User after_insert hook — auto-grant the Company User Permission so the
    new user immediately sees Department/Cost Center/etc. records linked to
    the school's company.
    """
    if doc.user_type != "System User":
        return
    if doc.name in ("Administrator", "Guest"):
        return
    try:
        company = _company()
    except RuntimeError:
        return  # Setup wizard not yet run; do nothing
    _insert_company_user_permission(doc.name, company)


def grant_school_role_perms():
    """Create DocPerm rows for each School role on the doctypes they need.

    Custom roles created in code start with ZERO doctype permissions, so
    users assigned only a School role can't read Department/Cost Center
    (which caused the empty dropdown bug). This function backfills the
    permissions. Idempotent — skips any (doctype, role) that already has a
    DocPerm row.
    """
    created = 0
    for role, dt_perms in SCHOOL_ROLE_DOCPERMS.items():
        if not frappe.db.exists("Role", role):
            continue
        for doctype, perms in dt_perms:
            if not frappe.db.exists("DocType", doctype):
                continue
            existing = frappe.db.exists(
                "Custom DocPerm", {"parent": doctype, "role": role}
            )
            if existing:
                continue
            doc = {
                "doctype": "Custom DocPerm",
                "parent": doctype,
                "parenttype": "DocType",
                "parentfield": "permissions",
                "role": role,
                "permlevel": 0,
            }
            doc.update(perms)
            frappe.get_doc(doc).insert(ignore_permissions=True)
            created += 1
    # Clear permission cache so the new perms take effect without a restart
    frappe.clear_cache()
    print(f"grant_school_role_perms: created {created} new DocPerm rows")


def rebuild_school_docperms():
    """Authoritatively rebuild ALL Custom DocPerm rows for School roles from
    SCHOOL_ROLE_DOCPERMS (delete-then-recreate).

    grant_school_role_perms() is create-if-missing and will NOT upgrade an
    existing (doctype, role) row — so changed rights (e.g. Stores gaining MR
    write + RFQ/Supplier Quotation, or new roles) won't take. This function
    makes the dict the single source of truth. Safe: the delete + recreate
    happen in one transaction; access is restored immediately.
    """
    roles = list(SCHOOL_ROLE_DOCPERMS.keys())
    deleted = 0
    for role in roles:
        rows = frappe.db.sql_list(
            "select name from `tabCustom DocPerm` where role=%s", role
        )
        for name in rows:
            frappe.delete_doc("Custom DocPerm", name, ignore_permissions=True, force=True)
            deleted += 1
    created = 0
    for role, dt_perms in SCHOOL_ROLE_DOCPERMS.items():
        if not frappe.db.exists("Role", role):
            continue
        for doctype, perms in dt_perms:
            if not frappe.db.exists("DocType", doctype):
                continue
            doc = {
                "doctype": "Custom DocPerm",
                "parent": doctype,
                "parenttype": "DocType",
                "parentfield": "permissions",
                "role": role,
                "permlevel": 0,
            }
            doc.update(perms)
            frappe.get_doc(doc).insert(ignore_permissions=True)
            created += 1
    frappe.clear_cache()
    print(f"rebuild_school_docperms: deleted {deleted}, recreated {created} DocPerm rows")


def setup_all():
    """Run structural setup only (depts, CCs, roles, custom fields, workflow).

    Called automatically on `bench install-app rdschool` via the after_install
    hook. Safe for production — does NOT create demo users, sample suppliers,
    or sample items. To add those (for staging/dev), call seed_demo_data()
    separately or set `bench --site <site> set-config rdschool_seed_demo_data 1`
    before installing.
    """
    create_departments()
    create_cost_centers()
    create_role_profiles()
    ensure_role_profile_roles()  # upgrade existing profiles to match declared roles
    create_school_roles_and_assign()  # Roles only; users are demo data
    rebuild_school_docperms()  # authoritative (handles upgrades, not just new)
    ensure_company_user_permissions()
    create_item_groups()
    create_supplier_groups()
    create_mr_custom_fields()
    create_mr_workflow()
    migrate_mr_workflow_states()  # remap any in-flight MRs to the new states
    create_mr_notifications()
    if frappe.conf.get("rdschool_seed_demo_data"):
        seed_demo_data()
    frappe.db.commit()
    print("setup_all: complete")


def seed_demo_data():
    """Add sample suppliers, items, and demo users (Anita Teacher, Ravi
    Principal, etc.). For dev/staging only — never call on production where
    real users will sign in."""
    create_suppliers()
    create_items()
    create_demo_users()
    print("seed_demo_data: complete")


def create_departments():
    """Create the 13 school departments. Idempotent.

    Note: ERPNext auto-suffixes Department names with " - {company_abbr}",
    so we look up by the dict form on department_name + company instead of
    by name.
    """
    parent = "All Departments"
    if not frappe.db.exists("Department", parent):
        frappe.get_doc(
            {
                "doctype": "Department",
                "department_name": parent,
                "is_group": 1,
            }
        ).insert(ignore_permissions=True)

    created = 0
    for name in DEPARTMENTS:
        if frappe.db.exists(
            {"doctype": "Department", "department_name": name, "company": _company()}
        ):
            continue
        frappe.get_doc(
            {
                "doctype": "Department",
                "department_name": name,
                "parent_department": parent,
                "company": _company(),
                "is_group": 0,
            }
        ).insert(ignore_permissions=True)
        created += 1
    print(f"create_departments: created {created} new (total {len(DEPARTMENTS)})")


def create_cost_centers():
    """Create one cost center per department under the Company's root group.

    Parent is the company-named root group ("RD School Betul - RSB"), not
    "Main - RSB" — Main is a leaf node used for posting, not a group.
    """
    parent = f"{_company()} - {_abbr()}"
    if not frappe.db.exists("Cost Center", parent):
        raise RuntimeError(f"Expected root cost center {parent!r} not found")

    created = 0
    for dept in DEPARTMENTS:
        cc_name = f"{dept} - {_abbr()}"
        if frappe.db.exists("Cost Center", cc_name):
            continue
        frappe.get_doc(
            {
                "doctype": "Cost Center",
                "cost_center_name": dept,
                "parent_cost_center": parent,
                "company": _company(),
                "is_group": 0,
            }
        ).insert(ignore_permissions=True)
        created += 1
    print(f"create_cost_centers: created {created} new (total {len(DEPARTMENTS)})")


def create_role_profiles():
    """Create the 6 school-specific Role Profiles. Idempotent.

    Each Role Profile aggregates the listed roles. We do NOT create new Role
    docs — we reuse ERPNext built-ins where possible.
    """
    created = 0
    for profile_name, roles in ROLE_PROFILES.items():
        if frappe.db.exists("Role Profile", profile_name):
            continue
        # Confirm each role exists; create as a basic role if not
        for role in roles:
            if not frappe.db.exists("Role", role):
                frappe.get_doc({"doctype": "Role", "role_name": role}).insert(
                    ignore_permissions=True
                )
        frappe.get_doc(
            {
                "doctype": "Role Profile",
                "role_profile": profile_name,
                "roles": [{"role": r} for r in roles],
            }
        ).insert(ignore_permissions=True)
        created += 1
    print(f"create_role_profiles: created {created} new (total {len(ROLE_PROFILES)})")


def ensure_role_profile_roles():
    """Add any missing roles to EXISTING Role Profiles to match ROLE_PROFILES.

    create_role_profiles() is create-if-missing and will not update a profile
    that already exists. This routine reconciles existing profiles with the
    declared role list (e.g. upgrading School Stores Incharge from Purchase
    User to Purchase Manager). Idempotent — only appends missing roles, never
    removes. Also ensures the named Role docs exist.
    """
    changed = 0
    for profile_name, roles in ROLE_PROFILES.items():
        if not frappe.db.exists("Role Profile", profile_name):
            continue
        for role in roles:
            if not frappe.db.exists("Role", role):
                frappe.get_doc(
                    {"doctype": "Role", "role_name": role, "desk_access": 1}
                ).insert(ignore_permissions=True)
        prof = frappe.get_doc("Role Profile", profile_name)
        existing = {r.role for r in prof.roles}
        missing = [r for r in roles if r not in existing]
        if missing:
            for r in missing:
                prof.append("roles", {"role": r})
            prof.save(ignore_permissions=True)
            changed += 1
            print(f"  upgraded profile {profile_name!r}: added {missing}")
    print(f"ensure_role_profile_roles: updated {changed} existing profiles")


def create_demo_users():
    """Create one demo User per role for testing. Idempotent."""
    created = 0
    for email, full_name, role_profile, dept in DEMO_USERS:
        if frappe.db.exists("User", email):
            continue
        first, _, last = full_name.partition(" ")
        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": email,
                "first_name": first,
                "last_name": last or "",
                "send_welcome_email": 0,
                "new_password": _demo_password(),
                "user_type": "System User",
                "enabled": 1,
                "role_profile_name": role_profile,
                "language": "en",
                "time_zone": "Asia/Kolkata",
            }
        )
        user.insert(ignore_permissions=True)
        # Department on User doc (optional FYI; for HR linking we'd create an Employee)
        if frappe.get_meta("User").has_field("department"):
            frappe.db.set_value("User", email, "department", dept)
        created += 1
    print(f"create_demo_users: created {created} new (total {len(DEMO_USERS)})")


def create_school_roles_and_assign():
    """Create school-specific Roles (matching role-profile names) and assign
    each demo user to their corresponding role.

    The workflow gates on these Roles, not on Role Profiles — Frappe's
    Workflow `allowed` field links to Role, not Role Profile.
    """
    role_names = list(ROLE_PROFILES.keys())
    created_roles = 0
    for r in role_names:
        if not frappe.db.exists("Role", r):
            frappe.get_doc({"doctype": "Role", "role_name": r, "desk_access": 1}).insert(
                ignore_permissions=True
            )
            created_roles += 1

    # Assign each demo user the role matching their role profile name by
    # inserting Has Role rows directly. The User.add_roles / User.save path
    # was silently dropping appended roles on this site (Frappe v15 behavior
    # around role_profile_name overriding manual roles).
    assigned = 0
    for email, _name, role_profile, _dept in DEMO_USERS:
        if not frappe.db.exists("User", email):
            continue
        if frappe.db.exists("Has Role", {"parent": email, "role": role_profile}):
            continue
        frappe.get_doc(
            {
                "doctype": "Has Role",
                "parent": email,
                "parenttype": "User",
                "parentfield": "roles",
                "role": role_profile,
            }
        ).insert(ignore_permissions=True)
        assigned += 1
    print(
        f"create_school_roles_and_assign: created {created_roles} roles, "
        f"assigned to {assigned} users"
    )


def create_supplier_groups():
    """Create supplier groups under the 'All Supplier Groups' root."""
    parent = "All Supplier Groups"
    if not frappe.db.exists("Supplier Group", parent):
        raise RuntimeError(f"Root supplier group {parent!r} missing")
    created = 0
    for name in SUPPLIER_GROUPS:
        if frappe.db.exists("Supplier Group", name):
            continue
        frappe.get_doc(
            {
                "doctype": "Supplier Group",
                "supplier_group_name": name,
                "parent_supplier_group": parent,
                "is_group": 0,
            }
        ).insert(ignore_permissions=True)
        created += 1
    print(f"create_supplier_groups: created {created} new (total {len(SUPPLIER_GROUPS)})")


def create_suppliers():
    """Create sample suppliers. Naming is by supplier_name (autoname rule)."""
    created = 0
    for sname, sgroup, country, currency in SUPPLIERS:
        if frappe.db.exists("Supplier", sname):
            continue
        frappe.get_doc(
            {
                "doctype": "Supplier",
                "supplier_name": sname,
                "supplier_group": sgroup,
                "country": country,
                "default_currency": currency,
                "supplier_type": "Company",
            }
        ).insert(ignore_permissions=True)
        created += 1
    print(f"create_suppliers: created {created} new (total {len(SUPPLIERS)})")


def create_item_groups():
    """Create item groups under 'All Item Groups'."""
    parent = "All Item Groups"
    if not frappe.db.exists("Item Group", parent):
        raise RuntimeError(f"Root item group {parent!r} missing")
    created = 0
    for name in ITEM_GROUPS:
        if frappe.db.exists("Item Group", name):
            continue
        frappe.get_doc(
            {
                "doctype": "Item Group",
                "item_group_name": name,
                "parent_item_group": parent,
                "is_group": 0,
            }
        ).insert(ignore_permissions=True)
        created += 1
    print(f"create_item_groups: created {created} new (total {len(ITEM_GROUPS)})")


def create_items():
    """Create sample items. Box UOM is created if missing."""
    for extra_uom in ("Box",):
        if not frappe.db.exists("UOM", extra_uom):
            frappe.get_doc({"doctype": "UOM", "uom_name": extra_uom}).insert(
                ignore_permissions=True
            )

    created = 0
    for code, name, group, uom, stock_uom, is_stock, rate in ITEMS:
        if frappe.db.exists("Item", code):
            continue
        frappe.get_doc(
            {
                "doctype": "Item",
                "item_code": code,
                "item_name": name,
                "item_group": group,
                "stock_uom": stock_uom,
                "is_stock_item": is_stock,
                "include_item_in_manufacturing": 0,
                "standard_rate": rate,
                "uoms": [{"uom": uom, "conversion_factor": 1}],
                "item_defaults": [{"company": _company()}],
            }
        ).insert(ignore_permissions=True)
        created += 1
    print(f"create_items: created {created} new (total {len(ITEMS)})")


# ---------------------------------------------------------------------------
# Phase 3A: Custom fields on Material Request
# ---------------------------------------------------------------------------

MR_CUSTOM_FIELDS = {
    "Material Request": [
        {
            "fieldname": "rsb_school_section",
            "label": "RD School Details",
            "fieldtype": "Section Break",
            "insert_after": "schedule_date",
            "collapsible": 0,
        },
        {
            "fieldname": "rsb_school_department",
            "label": "School Department",
            "fieldtype": "Link",
            "options": "Department",
            "reqd": 1,
            "in_list_view": 1,
            "in_standard_filter": 1,
            "insert_after": "rsb_school_section",
            # Restrict dropdown to the current company's departments only,
            # hiding the ERPNext-default depts (Research & Development, etc.)
            # that aren't relevant to the school.
            "link_filters": '[["Department","company","=","{company}"]]',
        },
        {
            "fieldname": "rsb_cost_center",
            "label": "Cost Center",
            "fieldtype": "Link",
            "options": "Cost Center",
            "reqd": 1,
            "insert_after": "rsb_school_department",
            "description": "Cost center is used for budget tracking. "
            "Set on each MR item line; carried forward to PO/PR/PI automatically.",
            "link_filters": (
                '[["Cost Center","company","=","{company}"],'
                '["Cost Center","is_group","=",0]]'
            ),
        },
        {
            "fieldname": "rsb_col_break_school",
            "fieldtype": "Column Break",
            "insert_after": "rsb_cost_center",
        },
        {
            "fieldname": "rsb_academic_year",
            "label": "Academic Year",
            "fieldtype": "Data",
            "reqd": 1,
            "default": "2026-2027",
            "insert_after": "rsb_col_break_school",
        },
        {
            "fieldname": "rsb_reason_for_request",
            "label": "Reason for Request",
            "fieldtype": "Small Text",
            "reqd": 1,
            "insert_after": "rsb_academic_year",
        },
        # --- Multi-stage SOP routing fields (Phase B) ---
        {
            "fieldname": "rsb_routing_section",
            "label": "Procurement Routing",
            "fieldtype": "Section Break",
            "insert_after": "rsb_reason_for_request",
            "collapsible": 0,
        },
        {
            # Drives the VP exemption bypass (T2 vs T3). Set by HOD at
            # creation, confirmable by VP. "Standard" routes through Store;
            # any Non-Quotation value bypasses Store straight to Principal.
            "fieldname": "rsb_purchase_category",
            "label": "Purchase Category",
            "fieldtype": "Select",
            "options": "Standard\nNon-Quotation - Direct\nNon-Quotation - Urgent",
            "default": "Standard",
            "reqd": 1,
            "in_standard_filter": 1,
            "insert_after": "rsb_routing_section",
        },
        {
            # Set by Store while MR is in Pending Store Verification; drives
            # the in-stock (T6) vs out-of-stock/RFQ (T7) branch. Blank by
            # default so Store must make an explicit choice.
            "fieldname": "rsb_stock_availability",
            "label": "Stock Availability (set by Store)",
            "fieldtype": "Select",
            "options": "\nIn Stock\nOut of Stock",
            "insert_after": "rsb_purchase_category",
            "in_standard_filter": 1,
        },
        {
            "fieldname": "rsb_routing_col_break",
            "fieldtype": "Column Break",
            "insert_after": "rsb_stock_availability",
        },
        {
            # Reviewer notes captured on Revise/Reject/Hold so the requester
            # knows why. Free text, optional.
            "fieldname": "rsb_approval_remarks",
            "label": "Approval / Review Remarks",
            "fieldtype": "Small Text",
            "insert_after": "rsb_routing_col_break",
        },
        # --- RFQ / quotation integration links (Phase C) ---
        {
            "fieldname": "rsb_request_for_quotation",
            "label": "Request for Quotation",
            "fieldtype": "Link",
            "options": "Request for Quotation",
            "read_only": 1,
            "insert_after": "rsb_approval_remarks",
            "description": "Set by Store on the out-of-stock branch.",
        },
        {
            "fieldname": "rsb_selected_supplier_quotation",
            "label": "Selected Supplier Quotation",
            "fieldtype": "Link",
            "options": "Supplier Quotation",
            "insert_after": "rsb_request_for_quotation",
            "description": "The winning quote from the comparison.",
        },
        {
            "fieldname": "rsb_selected_supplier",
            "label": "Selected Supplier",
            "fieldtype": "Link",
            "options": "Supplier",
            "read_only": 1,
            "fetch_from": "rsb_selected_supplier_quotation.supplier",
            "insert_after": "rsb_selected_supplier_quotation",
        },
    ]
}


def create_mr_custom_fields():
    """Add school-specific custom fields to Material Request.

    Substitutes the active Company name into any `{company}` placeholder in
    `link_filters` strings before creating the fields. This lets the JSON
    filter survive being re-applied on another company without code edits.
    """
    from copy import deepcopy
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

    company = _company()
    fields = deepcopy(MR_CUSTOM_FIELDS)
    for doctype_fields in fields.values():
        for f in doctype_fields:
            if "link_filters" in f and "{company}" in f["link_filters"]:
                f["link_filters"] = f["link_filters"].format(company=company)
    create_custom_fields(fields, ignore_validate=True)
    print(
        f"create_mr_custom_fields: ensured {sum(len(v) for v in fields.values())} fields"
    )


# ---------------------------------------------------------------------------
# Multi-stage Material Request approval workflow (SOP Phase 1)
# ---------------------------------------------------------------------------
#
# Flow: HOD/Teacher Draft -> VP Review -> (Standard) Store Verification ->
#       (in stock) Principal / (out of stock) RFQ -> Principal Decision ->
#       Approved (ds1, unlocks native Create->PO). Non-Quotation bypasses
#       Store straight to Principal. Revise loops stay docstatus 0; only
#       Approved is ds1; Rejected/Closed are soft ds0 terminals.
#
# Workflow NAME is kept ("MR Approval - RSB") so the in-place migration only
# has to remap old state values (see migrate_mr_workflow_states).

MR_WORKFLOW_NAME = "MR Approval - RSB"

# Roles that may raise/edit a draft requisition (decision: both can raise).
REQUESTER_ROLES = ["School Teacher", "School HOD"]
# Combined final-decision gate (Principal + thin Director co-approver).
PRINCIPAL_GATE_ROLES = ["School Principal", "School Director"]

# A state listed MORE THAN ONCE with different allow_edit roles grants edit
# to ALL those roles — Frappe's get_document_state_roles() collects allow_edit
# from every state row matching the name. We use this so Draft is editable by
# both requester roles and the Principal-decision state by Principal+Director.
MR_WORKFLOW_STATES = [
    # (state, doc_status, allow_edit_role, style)
    ("Draft", 0, "School Teacher", "Primary"),
    ("Draft", 0, "School HOD", "Primary"),
    ("Pending VP Review", 0, "School Vice Principal", "Warning"),
    ("Pending Store Verification", 0, "School Stores Incharge", "Info"),
    ("RFQ In Progress", 0, "School Stores Incharge", "Info"),
    ("Pending Principal Decision", 0, "School Principal", "Warning"),
    ("Pending Principal Decision", 0, "School Director", "Warning"),
    ("On Hold", 0, "School Principal", "Warning"),
    ("Approved", 1, "School Stores Incharge", "Success"),
    ("Rejected", 0, "School HOD", "Danger"),
    ("Closed", 0, "School Principal", "Danger"),
]

MR_WORKFLOW_TRANSITIONS = [
    # dicts: from, action, to, allowed (str or list of roles), condition (opt).
    # A list 'allowed' expands to one Workflow Transition row per role.
    {"from": "Draft", "action": "Submit for VP Review",
     "to": "Pending VP Review", "allowed": REQUESTER_ROLES},

    # VP conditional split on Purchase Category (the SOP exemption bypass).
    {"from": "Pending VP Review", "action": "Accept → Store",
     "to": "Pending Store Verification", "allowed": "School Vice Principal",
     "condition": 'doc.rsb_purchase_category == "Standard"'},
    {"from": "Pending VP Review", "action": "Accept → Direct (Exemption)",
     "to": "Pending Principal Decision", "allowed": "School Vice Principal",
     "condition": 'doc.rsb_purchase_category and doc.rsb_purchase_category != "Standard"'},
    {"from": "Pending VP Review", "action": "Revise (send to HOD)",
     "to": "Draft", "allowed": "School Vice Principal"},
    {"from": "Pending VP Review", "action": "Reject",
     "to": "Rejected", "allowed": "School Vice Principal"},

    # Store stock split on Stock Availability.
    {"from": "Pending Store Verification", "action": "In-Stock → Principal",
     "to": "Pending Principal Decision", "allowed": "School Stores Incharge",
     "condition": 'doc.rsb_stock_availability == "In Stock"'},
    {"from": "Pending Store Verification", "action": "Out-of-Stock → Raise RFQ",
     "to": "RFQ In Progress", "allowed": "School Stores Incharge",
     "condition": 'doc.rsb_stock_availability == "Out of Stock"'},

    {"from": "RFQ In Progress", "action": "Comparison Ready → Principal",
     "to": "Pending Principal Decision", "allowed": "School Stores Incharge"},
    {"from": "RFQ In Progress", "action": "Revise (send to HOD)",
     "to": "Draft", "allowed": "School Stores Incharge"},

    # Principal/Director decision gate (each action expands to 2 role rows).
    {"from": "Pending Principal Decision", "action": "Accept (authorize PO)",
     "to": "Approved", "allowed": PRINCIPAL_GATE_ROLES},
    {"from": "Pending Principal Decision", "action": "Hold",
     "to": "On Hold", "allowed": PRINCIPAL_GATE_ROLES},
    {"from": "Pending Principal Decision", "action": "Revise → VP",
     "to": "Pending VP Review", "allowed": PRINCIPAL_GATE_ROLES},
    {"from": "Pending Principal Decision", "action": "Reject (close file)",
     "to": "Closed", "allowed": PRINCIPAL_GATE_ROLES},

    {"from": "On Hold", "action": "Resume → Decision",
     "to": "Pending Principal Decision", "allowed": PRINCIPAL_GATE_ROLES},
    {"from": "On Hold", "action": "Reject (close file)",
     "to": "Closed", "allowed": PRINCIPAL_GATE_ROLES},

    # Rejected can be reopened by a requester (Closed is permanent).
    {"from": "Rejected", "action": "Resubmit (reopen)",
     "to": "Draft", "allowed": REQUESTER_ROLES},
]

# Style per state name, for the Workflow State master docs.
_MR_STATE_STYLE = {s: style for s, _ds, _role, style in MR_WORKFLOW_STATES}


def _expanded_transitions():
    """Yield (from, action, to, allowed_role, condition) expanding any list
    'allowed' into one row per role."""
    for t in MR_WORKFLOW_TRANSITIONS:
        allowed = t["allowed"]
        roles = allowed if isinstance(allowed, list) else [allowed]
        for role in roles:
            yield (t["from"], t["action"], t["to"], role, t.get("condition"))


def create_mr_workflow():
    """Create/replace the multi-stage Material Request workflow. Idempotent —
    drops and recreates so re-runs reflect the latest definition.
    """
    # Ensure each distinct Workflow State master exists.
    for state in {s for s, _ds, _role, _style in MR_WORKFLOW_STATES}:
        if not frappe.db.exists("Workflow State", state):
            frappe.get_doc(
                {
                    "doctype": "Workflow State",
                    "workflow_state_name": state,
                    "style": _MR_STATE_STYLE.get(state, "Primary"),
                }
            ).insert(ignore_permissions=True)

    # Ensure each distinct Workflow Action Master exists.
    for action in {t["action"] for t in MR_WORKFLOW_TRANSITIONS}:
        if not frappe.db.exists("Workflow Action Master", action):
            frappe.get_doc(
                {"doctype": "Workflow Action Master", "workflow_action_name": action}
            ).insert(ignore_permissions=True)

    if frappe.db.exists("Workflow", MR_WORKFLOW_NAME):
        frappe.delete_doc(
            "Workflow", MR_WORKFLOW_NAME, ignore_permissions=True, force=True
        )

    workflow = frappe.get_doc(
        {
            "doctype": "Workflow",
            "workflow_name": MR_WORKFLOW_NAME,
            "document_type": "Material Request",
            "workflow_state_field": "workflow_state",
            "is_active": 1,
            "send_email_alert": 1,
            "states": [
                {"state": s, "doc_status": str(ds), "allow_edit": role}
                for s, ds, role, _ in MR_WORKFLOW_STATES
            ],
            "transitions": [
                {
                    "state": frm,
                    "action": act,
                    "next_state": to,
                    "allowed": role,
                    "condition": cond or "",
                    "allow_self_approval": 1,
                }
                for frm, act, to, role, cond in _expanded_transitions()
            ],
        }
    )
    workflow.insert(ignore_permissions=True)
    print(f"create_mr_workflow: created workflow {MR_WORKFLOW_NAME!r}")


# Map from OLD single-stage states to NEW multi-stage states for in-flight docs.
# Draft / Approved / Rejected exist in both workflows (unchanged). Only the old
# "Pending Approval" disappears and is remapped to "Pending Principal Decision"
# (preserves "awaiting top-authority" intent; both are docstatus 0).
MR_STATE_MIGRATION_MAP = {
    "Pending Approval": "Pending Principal Decision",
}


def migrate_mr_workflow_states():
    """Remap in-flight Material Requests from the old single-stage workflow
    states to the new multi-stage states, and backfill the new mandatory
    rsb_purchase_category field. Run AFTER create_mr_workflow().

    Safe & idempotent: only updates rows whose workflow_state is an old name.
    Does NOT touch docstatus (the remap is ds0->ds0). Submitted/Approved docs
    keep their state. Asserts no orphan states remain in the new workflow.
    """
    valid_states = {s for s, _ds, _role, _style in MR_WORKFLOW_STATES}

    # Backfill the new mandatory Select so existing MRs validate on next save.
    backfilled = frappe.db.sql(
        "update `tabMaterial Request` set rsb_purchase_category='Standard' "
        "where ifnull(rsb_purchase_category,'')=''"
    )

    remapped = 0
    for old_state, new_state in MR_STATE_MIGRATION_MAP.items():
        names = frappe.db.sql_list(
            "select name from `tabMaterial Request` where workflow_state=%s",
            old_state,
        )
        for name in names:
            frappe.db.set_value(
                "Material Request", name, "workflow_state", new_state,
                update_modified=False,
            )
            remapped += 1

    # Orphan assertion: any MR on a state the new workflow doesn't define would
    # be stranded (no transitions, read-only for all). Fail loudly if so.
    orphans = frappe.db.sql(
        "select distinct workflow_state from `tabMaterial Request` "
        "where ifnull(workflow_state,'')!='' and workflow_state not in %s",
        (tuple(valid_states),),
        as_dict=1,
    )
    orphan_states = [o["workflow_state"] for o in orphans]
    frappe.db.commit()
    print(
        f"migrate_mr_workflow_states: remapped {remapped} MRs, "
        f"backfilled category on existing MRs."
    )
    if orphan_states:
        print(
            f"  WARNING: {len(orphan_states)} orphan state(s) not in new "
            f"workflow: {orphan_states} — these MRs will be read-only until "
            f"remapped. Add them to MR_STATE_MIGRATION_MAP."
        )
    else:
        print("  No orphan states — all in-flight MRs are on valid states.")
    return {"remapped": remapped, "orphans": orphan_states}


# ---------------------------------------------------------------------------
# Phase 3C: In-app notifications on workflow transitions
# ---------------------------------------------------------------------------

# (name, condition, recipients_spec, subject_template, message_template)
# recipients_spec is a list of dicts mirroring Notification.recipients child table.
_MR_DETAIL_BLOCK = (
    "<p><b>Department:</b> {{ doc.rsb_school_department }}<br>"
    "<b>Cost Center:</b> {{ doc.rsb_cost_center }}<br>"
    "<b>Category:</b> {{ doc.rsb_purchase_category }}<br>"
    "<b>Reason:</b> {{ doc.rsb_reason_for_request }}<br>"
    "<b>Required by:</b> {{ doc.schedule_date }}</p>"
)

# Per-handoff in-app notifications, one per new workflow state. Each notifies
# the role that must act NEXT (or the requester for back-to-you outcomes).
# "back to requester" uses receiver_by_document_field=owner (single person),
# never role fan-out, to avoid the duplicate-notification problem.
MR_NOTIFICATIONS = [
    {
        "name": "MR Pending VP Review - RSB",
        "condition": "doc.workflow_state == 'Pending VP Review'",
        "recipients": [{"receiver_by_role": "School Vice Principal"}],
        "subject": "Material Request {{ doc.name }} pending VP review",
        "message": (
            "<p>A Material Request <b>{{ doc.name }}</b> needs your first-level "
            "review.</p>" + _MR_DETAIL_BLOCK +
            "<p>Accept → Store, Accept → Direct (exemption), Revise, or Reject.</p>"
        ),
    },
    {
        "name": "MR Pending Store Verification - RSB",
        "condition": "doc.workflow_state == 'Pending Store Verification'",
        "recipients": [{"receiver_by_role": "School Stores Incharge"}],
        "subject": "Material Request {{ doc.name }} pending stock verification",
        "message": (
            "<p>Material Request <b>{{ doc.name }}</b> was accepted by the Vice "
            "Principal and needs stock verification.</p>" + _MR_DETAIL_BLOCK +
            "<p>Set Stock Availability, then route In-Stock → Principal or "
            "Out-of-Stock → Raise RFQ.</p>"
        ),
    },
    {
        "name": "MR RFQ In Progress - RSB",
        "condition": "doc.workflow_state == 'RFQ In Progress'",
        "recipients": [{"receiver_by_role": "School Stores Incharge"}],
        "subject": "Material Request {{ doc.name }} — raise RFQ & compare quotes",
        "message": (
            "<p>Material Request <b>{{ doc.name }}</b> is out of stock. Raise a "
            "Request for Quotation, collect Supplier Quotations, compare, then "
            "send the comparison up to the Principal.</p>"
        ),
    },
    {
        "name": "MR Pending Principal Decision - RSB",
        "condition": "doc.workflow_state == 'Pending Principal Decision'",
        "recipients": [
            {"receiver_by_role": "School Principal"},
            {"receiver_by_role": "School Director"},
        ],
        "subject": "Material Request {{ doc.name }} pending final decision",
        "message": (
            "<p>Material Request <b>{{ doc.name }}</b> has reached the final "
            "decision gate.</p>" + _MR_DETAIL_BLOCK +
            "<p>Accept (authorize PO), Hold, Revise → VP, or Reject (close).</p>"
        ),
    },
    {
        "name": "MR Approved - RSB",
        "condition": "doc.workflow_state == 'Approved'",
        "recipients": [{"receiver_by_role": "School Stores Incharge"}],
        "subject": "Material Request {{ doc.name }} approved — create PO",
        "message": (
            "<p>Material Request <b>{{ doc.name }}</b> has been approved.</p>"
            "<p>As Purchase Manager, create the Purchase Order from it "
            "(Create → Purchase Order).</p>"
        ),
    },
    {
        "name": "MR On Hold - RSB",
        "condition": "doc.workflow_state == 'On Hold'",
        "recipients": [{"receiver_by_document_field": "owner"}],
        "subject": "Material Request {{ doc.name }} put on hold",
        "message": (
            "<p>Your Material Request <b>{{ doc.name }}</b> has been put on hold "
            "by the Principal. It remains in the management log pending review.</p>"
        ),
    },
    {
        "name": "MR Sent Back for Revision - RSB",
        "condition": "doc.workflow_state == 'Draft' and doc.docstatus == 0",
        "recipients": [{"receiver_by_document_field": "owner"}],
        "subject": "Material Request {{ doc.name }} sent back for revision",
        "message": (
            "<p>Material Request <b>{{ doc.name }}</b> was sent back for "
            "revision.</p><p>{% if doc.rsb_approval_remarks %}<b>Remarks:</b> "
            "{{ doc.rsb_approval_remarks }}<br>{% endif %}Edit and submit for "
            "review again.</p>"
        ),
    },
    {
        "name": "MR Rejected - RSB",
        "condition": "doc.workflow_state == 'Rejected'",
        "recipients": [{"receiver_by_document_field": "owner"}],
        "subject": "Your Material Request {{ doc.name }} was rejected",
        "message": (
            "<p>Your Material Request <b>{{ doc.name }}</b> was rejected by the "
            "Vice Principal.</p><p>{% if doc.rsb_approval_remarks %}<b>Remarks:</b> "
            "{{ doc.rsb_approval_remarks }}<br>{% endif %}You may reopen "
            "(Resubmit) and revise it.</p>"
        ),
    },
    {
        "name": "MR Closed - RSB",
        "condition": "doc.workflow_state == 'Closed'",
        "recipients": [{"receiver_by_document_field": "owner"}],
        "subject": "Material Request {{ doc.name }} closed",
        "message": (
            "<p>Your Material Request <b>{{ doc.name }}</b> has been permanently "
            "closed by the Principal.</p><p>{% if doc.rsb_approval_remarks %}"
            "<b>Remarks:</b> {{ doc.rsb_approval_remarks }}<br>{% endif %}"
            "Raise a fresh request if still required.</p>"
        ),
    },
]


def create_mr_notifications():
    """Create in-app (System Notification channel) alerts on MR state changes.

    Uses channel='System Notification' so notifications fire WITHOUT needing
    an SMTP / Email Account — they appear in the bell icon at top-right.
    Idempotent — drops and recreates each notification to reflect the latest
    template in this file.
    """
    created = 0
    for spec in MR_NOTIFICATIONS:
        if frappe.db.exists("Notification", spec["name"]):
            frappe.delete_doc(
                "Notification", spec["name"], ignore_permissions=True, force=True
            )
        doc = frappe.get_doc(
            {
                "doctype": "Notification",
                "name": spec["name"],
                "subject": spec["subject"],
                "document_type": "Material Request",
                "event": "Value Change",
                "value_changed": "workflow_state",
                "condition": spec["condition"],
                "channel": "System Notification",  # in-app bell, no SMTP needed
                "enabled": 1,
                "is_standard": 0,
                "send_system_notification": 1,
                "recipients": spec["recipients"],
                "message": spec["message"],
            }
        )
        doc.insert(ignore_permissions=True)
        created += 1
    print(f"create_mr_notifications: ensured {created} notifications")


# ---------------------------------------------------------------------------
# Phase 4B: End-to-end UAT
# ---------------------------------------------------------------------------

DEFAULT_WAREHOUSE = f"Stores - {_abbr()}"


def run_uat():
    """Drive the full MR -> PO -> PR -> PI flow programmatically, acting as
    each demo user in turn. Verifies that the workflow, custom fields,
    permissions, and standard ERPNext linkages all work together.
    """
    from frappe.model.workflow import apply_workflow
    from erpnext.stock.doctype.material_request.material_request import (
        make_purchase_order,
    )
    from erpnext.buying.doctype.purchase_order.purchase_order import (
        make_purchase_receipt,
        make_purchase_invoice,
    )

    hod = "hod1@rdschool.local"
    vp = "vp@rdschool.local"
    principal = "principal@rdschool.local"
    stores = "stores@rdschool.local"
    accountant = "accountant@rdschool.local"

    dept_name = frappe.db.get_value(
        "Department",
        {"department_name": "Science Lab", "company": _company()},
        "name",
    )
    cost_center = f"Science Lab - {_abbr()}"
    supplier = "MP Lab Supplies Indore"

    # Step 1 - HOD creates a draft MR (Standard category -> goes via Store)
    frappe.clear_cache(user=hod)
    frappe.set_user(hod)
    mr = frappe.get_doc(
        {
            "doctype": "Material Request",
            "material_request_type": "Purchase",
            "transaction_date": frappe.utils.today(),
            "schedule_date": frappe.utils.add_days(frappe.utils.today(), 7),
            "company": _company(),
            "rsb_school_department": dept_name,
            "rsb_cost_center": cost_center,
            "rsb_academic_year": "2026-2027",
            "rsb_reason_for_request": "Lab restocking for Class 9 chemistry practical",
            "rsb_purchase_category": "Standard",
            "items": [
                {
                    "item_code": "RSB-LAB-001",
                    "qty": 20,
                    "schedule_date": frappe.utils.add_days(frappe.utils.today(), 7),
                    "warehouse": DEFAULT_WAREHOUSE,
                },
                {
                    "item_code": "RSB-LAB-003",
                    "qty": 2,
                    "schedule_date": frappe.utils.add_days(frappe.utils.today(), 7),
                    "warehouse": DEFAULT_WAREHOUSE,
                },
            ],
        }
    )
    mr.insert()
    print(f"[UAT] 1/9 HOD created MR: {mr.name} (state={mr.workflow_state})")

    # Step 2 - HOD submits for VP review
    apply_workflow(mr, "Submit for VP Review")
    mr.reload()
    print(f"[UAT] 2/9 Submitted for VP review: state={mr.workflow_state}")

    # Step 3 - VP accepts -> Store (Standard category)
    frappe.clear_cache(user=vp)
    frappe.set_user(vp)
    apply_workflow(mr, "Accept → Store")
    mr.reload()
    print(f"[UAT] 3/9 VP accepted -> Store: state={mr.workflow_state}")

    # Step 4 - Store marks In Stock -> Principal
    frappe.clear_cache(user=stores)
    frappe.set_user(stores)
    mr.rsb_stock_availability = "In Stock"
    mr.save()
    apply_workflow(mr, "In-Stock → Principal")
    mr.reload()
    print(f"[UAT] 4/9 Store (In Stock) -> Principal: state={mr.workflow_state}")

    # Step 5 - Principal accepts (authorize PO) -> Approved (docstatus 1)
    frappe.clear_cache(user=principal)
    frappe.set_user(principal)
    apply_workflow(mr, "Accept (authorize PO)")
    mr.reload()
    print(
        f"[UAT] 5/9 Principal approved: state={mr.workflow_state} "
        f"docstatus={mr.docstatus}"
    )

    # Step 6 - Stores creates Purchase Order from MR
    frappe.clear_cache(user=stores)
    frappe.set_user(stores)
    po = make_purchase_order(mr.name)
    po.supplier = supplier
    po.schedule_date = frappe.utils.add_days(frappe.utils.today(), 7)
    for item in po.items:
        item.schedule_date = po.schedule_date
        item.warehouse = DEFAULT_WAREHOUSE
    po = frappe.get_doc(po)  # reattach for save
    po.supplier = supplier
    po.insert()
    po.submit()
    print(f"[UAT] 6/9 Stores created & submitted PO: {po.name}")

    # Step 7 - Goods received -> Purchase Receipt
    pr = make_purchase_receipt(po.name)
    pr = frappe.get_doc(pr)
    for item in pr.items:
        item.warehouse = DEFAULT_WAREHOUSE
    pr.insert()
    pr.submit()
    print(f"[UAT] 7/9 Stores submitted PR (stock received): {pr.name}")

    # Step 8 - Accountant creates Purchase Invoice from PO
    frappe.clear_cache(user=accountant)
    frappe.set_user(accountant)
    pi = make_purchase_invoice(po.name)
    pi = frappe.get_doc(pi)
    pi.bill_no = f"BILL/{frappe.utils.today()}/001"
    pi.bill_date = frappe.utils.today()
    pi.insert()
    pi.submit()
    print(f"[UAT] 8/9 Accountant submitted PI: {pi.name}")

    # Step 9 - Summary
    frappe.set_user("Administrator")
    print(f"[UAT] 9/9 DONE. Pipeline: {mr.name} -> {po.name} -> {pr.name} -> {pi.name}")
    print(
        f"       Supplier: {supplier} | Items: {len(mr.items)} | "
        f"Total PI: {pi.grand_total} {pi.currency}"
    )
    return {"mr": mr.name, "po": po.name, "pr": pr.name, "pi": pi.name}
