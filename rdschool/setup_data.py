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
    "School Stores Incharge": [
        "Employee",
        "Stock Manager",
        "Purchase User",
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
}

DEMO_USERS = [
    ("teacher1@rdschool.local", "Anita Teacher", "School Teacher", "Science Lab"),
    ("principal@rdschool.local", "Ravi Principal", "School Principal", "Administration"),
    ("stores@rdschool.local", "Suresh Stores", "School Stores Incharge", "Stores & Procurement"),
    ("accountant@rdschool.local", "Priya Accounts", "School Accountant", "Accounts & Finance"),
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
        ("Material Request", {"read": 1, "print": 1, "report": 1}),
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
        ("Purchase Order", {"read": 1, "print": 1, "report": 1}),
        ("Purchase Receipt", {"read": 1, "print": 1, "report": 1}),
        ("Purchase Invoice", {"read": 1, "print": 1, "report": 1}),
        ("Payment Entry", {"read": 1, "print": 1, "report": 1}),
    ],
}


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
    create_school_roles_and_assign()  # Roles only; users are demo data
    grant_school_role_perms()
    create_item_groups()
    create_supplier_groups()
    create_mr_custom_fields()
    create_mr_workflow()
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
# Phase 3B: Approval Workflow on Material Request
# ---------------------------------------------------------------------------

# Single-approver flow per user's choice: Teacher → Principal → Approved.
MR_WORKFLOW_NAME = "MR Approval - RSB"

MR_WORKFLOW_STATES = [
    # (state, doc_status, allow_edit_role, style)
    # Note: Rejected is doc_status=0 (still a draft) because Frappe forbids
    # 0 -> 2 (cancel-without-submit). Rejection is a soft state — the teacher
    # can edit and re-submit, or the principal can amend.
    ("Draft", 0, "School Teacher", "Primary"),
    ("Pending Approval", 0, "School Principal", "Warning"),
    ("Approved", 1, "School Principal", "Success"),
    ("Rejected", 0, "School Principal", "Danger"),
]

MR_WORKFLOW_TRANSITIONS = [
    # (from_state, action, to_state, allowed_role)
    ("Draft", "Submit for Approval", "Pending Approval", "School Teacher"),
    ("Pending Approval", "Approve", "Approved", "School Principal"),
    # Principal can send the MR back to Draft for the Teacher to edit and
    # resubmit — softer than Reject (which closes the loop entirely).
    ("Pending Approval", "Send Back for Revision", "Draft", "School Principal"),
    ("Pending Approval", "Reject", "Rejected", "School Principal"),
    # After revision, Teacher resubmits via the same Draft -> Pending Approval
    # action. Rejected docs can also be re-edited and resubmitted (docstatus
    # is still 0); the Teacher just transitions Rejected -> Draft via the
    # Resubmit action below, then submits for approval again.
    ("Rejected", "Resubmit", "Draft", "School Teacher"),
]


def create_mr_workflow():
    """Create the Material Request approval workflow. Idempotent — drops and
    recreates the workflow if it already exists, so re-runs always reflect
    the latest definition in this file.
    """
    # Ensure each Workflow State exists (Frappe ships defaults but make sure)
    for state, _ds, _role, style in MR_WORKFLOW_STATES:
        if not frappe.db.exists("Workflow State", state):
            frappe.get_doc(
                {
                    "doctype": "Workflow State",
                    "workflow_state_name": state,
                    "style": style,
                }
            ).insert(ignore_permissions=True)

    # Ensure each Workflow Action Master exists for transition actions
    for _from, action, _to, _role in MR_WORKFLOW_TRANSITIONS:
        if not frappe.db.exists("Workflow Action Master", action):
            frappe.get_doc(
                {"doctype": "Workflow Action Master", "workflow_action_name": action}
            ).insert(ignore_permissions=True)

    # Drop existing workflow so we can recreate cleanly
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
            # In-app bell-icon notifications fire on every state transition.
            # Email notifications also fire IF an outgoing Email Account is
            # configured on the site (Settings > Email Domain / Email Account).
            "send_email_alert": 1,
            "states": [
                {
                    "state": s,
                    "doc_status": str(ds),
                    "allow_edit": role,
                }
                for s, ds, role, _ in MR_WORKFLOW_STATES
            ],
            "transitions": [
                {
                    "state": frm,
                    "action": act,
                    "next_state": to,
                    "allowed": role,
                    "allow_self_approval": 1,
                }
                for frm, act, to, role in MR_WORKFLOW_TRANSITIONS
            ],
        }
    )
    workflow.insert(ignore_permissions=True)
    print(f"create_mr_workflow: created workflow {MR_WORKFLOW_NAME!r}")


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

    teacher = "teacher1@rdschool.local"
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

    # Step 1 - Teacher creates a draft MR
    frappe.clear_cache(user=teacher)
    frappe.set_user(teacher)
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
            "items": [
                {
                    "item_code": "RSB-LAB-001",
                    "qty": 20,
                    "schedule_date": frappe.utils.add_days(
                        frappe.utils.today(), 7
                    ),
                    "warehouse": DEFAULT_WAREHOUSE,
                },
                {
                    "item_code": "RSB-LAB-003",
                    "qty": 2,
                    "schedule_date": frappe.utils.add_days(
                        frappe.utils.today(), 7
                    ),
                    "warehouse": DEFAULT_WAREHOUSE,
                },
            ],
        }
    )
    mr.insert()
    print(f"[UAT] 1/7 Teacher created MR: {mr.name} (workflow_state={mr.workflow_state})")

    # Step 2 - Teacher submits for approval
    apply_workflow(mr, "Submit for Approval")
    mr.reload()
    print(f"[UAT] 2/7 Submitted for approval: workflow_state={mr.workflow_state}")

    # Step 3 - Principal approves (this submits the doc -> docstatus 1)
    frappe.clear_cache(user=principal)
    frappe.set_user(principal)
    apply_workflow(mr, "Approve")
    mr.reload()
    print(
        f"[UAT] 3/7 Principal approved: workflow_state={mr.workflow_state} "
        f"docstatus={mr.docstatus}"
    )

    # Step 4 - Stores creates Purchase Order from MR
    frappe.clear_cache(user=stores)
    frappe.set_user(stores)
    po = make_purchase_order(mr.name)
    po.supplier = supplier
    po.schedule_date = frappe.utils.add_days(frappe.utils.today(), 7)
    for item in po.items:
        item.schedule_date = po.schedule_date
        item.warehouse = DEFAULT_WAREHOUSE
    po = frappe.get_doc(po)  # reattach for save
    po.insert()
    po.submit()
    print(f"[UAT] 4/7 Stores created & submitted PO: {po.name}")

    # Step 5 - Goods received -> Purchase Receipt
    pr = make_purchase_receipt(po.name)
    pr = frappe.get_doc(pr)
    for item in pr.items:
        item.warehouse = DEFAULT_WAREHOUSE
    pr.insert()
    pr.submit()
    print(f"[UAT] 5/7 Stores submitted PR (stock received): {pr.name}")

    # Step 6 - Accountant creates Purchase Invoice from PO
    frappe.clear_cache(user=accountant)
    frappe.set_user(accountant)
    pi = make_purchase_invoice(po.name)
    pi = frappe.get_doc(pi)
    pi.bill_no = f"BILL/{frappe.utils.today()}/001"
    pi.bill_date = frappe.utils.today()
    pi.insert()
    pi.submit()
    print(f"[UAT] 6/7 Accountant submitted PI: {pi.name}")

    # Step 7 - Summary
    frappe.set_user("Administrator")
    print(f"[UAT] 7/7 DONE. Pipeline: {mr.name} -> {po.name} -> {pr.name} -> {pi.name}")
    print(
        f"       Supplier: {supplier} | Items: {len(mr.items)} | "
        f"Total PI: {pi.grand_total} {pi.currency}"
    )
    return {"mr": mr.name, "po": po.name, "pr": pr.name, "pi": pi.name}
