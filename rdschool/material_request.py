"""Material Request and Purchase Order hooks for the rdschool app.

Wired via `doc_events` in hooks.py.
"""

import frappe


def copy_cost_center_to_items(doc, method=None):
    """Overwrite each MR item's cost_center with the header rsb_cost_center.

    ERPNext auto-fills item.cost_center with the company default ("Main - RSB")
    during insert, BEFORE this hook fires. So checking "only if empty" never
    triggers — we have to force-overwrite. The header field is the single
    source of truth for budget tracking on a school MR.
    """
    header_cc = doc.get("rsb_cost_center")
    if not header_cc:
        return
    for item in doc.get("items") or []:
        item.cost_center = header_cc


def copy_cost_center_from_mr(doc, method=None):
    """For each Purchase Order item, copy cost_center from the source Material
    Request Item (referenced by `material_request_item`).

    ERPNext's `make_purchase_order` mapping does not include cost_center, so
    new PO items lose the dept tagging we set on the MR. This hook restores it
    on every PO validate (cheap, idempotent).
    """
    for item in doc.get("items") or []:
        mr_item = item.get("material_request_item")
        if not mr_item:
            continue
        mr_cc = frappe.db.get_value("Material Request Item", mr_item, "cost_center")
        if mr_cc:
            item.cost_center = mr_cc
