"""Permission Query Conditions for the rdschool app.

Wired via `permission_query_conditions` in hooks.py.

Each function returns a SQL WHERE-clause snippet (no leading WHERE/AND) that
Frappe ANDs into list/report queries for the matching doctype.
"""

import frappe


PRIVILEGED_ROLES = {
    "Administrator",
    "System Manager",
    "School Principal",
    "School Stores Incharge",
    "School Accountant",
    "School Auditor",
}


def material_request_query(user=None):
    """Teachers see only their own MRs. Everyone else (privileged roles) sees
    all. Falls back to no-restriction for safety if the role lookup fails.
    """
    if not user:
        user = frappe.session.user
    if user == "Administrator":
        return ""

    roles = set(frappe.get_roles(user))
    if PRIVILEGED_ROLES & roles:
        return ""
    if "School Teacher" in roles:
        return f"`tabMaterial Request`.owner = {frappe.db.escape(user)}"
    return ""
