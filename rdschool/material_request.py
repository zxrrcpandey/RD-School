"""Material Request and Purchase Order hooks for the rdschool app.

Wired via `doc_events` in hooks.py.
"""

import frappe
from frappe import _


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


@frappe.whitelist()
def make_rfq_from_mr(material_request):
    """Create a draft Request for Quotation pre-filled with the MR's items and
    link it back to the MR (rsb_request_for_quotation).

    Why this exists: ERPNext's native "Create → Request for Quotation" button
    only appears on a SUBMITTED (docstatus 1) MR. In our workflow the MR stays
    a draft all through approval, so the Store can't use the native button on
    the out-of-stock branch. This whitelisted mapper builds the RFQ from the
    draft MR's items; the Store then adds suppliers and submits it.
    """
    mr = frappe.get_doc("Material Request", material_request)

    if mr.get("rsb_request_for_quotation"):
        frappe.throw(
            _("An RFQ ({0}) is already linked to this Material Request.").format(
                mr.rsb_request_for_quotation
            )
        )
    if not mr.get("items"):
        frappe.throw(_("This Material Request has no items."))

    rfq = frappe.new_doc("Request for Quotation")
    rfq.transaction_date = frappe.utils.today()
    rfq.company = mr.company
    rfq.message_for_supplier = (
        f"Please quote for the items in this RFQ (ref MR {mr.name})."
    )
    for it in mr.items:
        rfq.append(
            "items",
            {
                "item_code": it.item_code,
                "item_name": it.item_name,
                "description": it.description,
                "qty": it.qty,
                "uom": it.uom,
                "stock_uom": it.get("stock_uom") or it.uom,
                "conversion_factor": it.get("conversion_factor") or 1,
                "schedule_date": it.get("schedule_date") or mr.schedule_date,
                "warehouse": it.get("warehouse"),
                "material_request": mr.name,
                "material_request_item": it.name,
            },
        )
    # ignore_mandatory: RFQ requires at least one supplier, but we want to
    # hand the Store a draft with the items already filled — they add the
    # 2-3 suppliers in the form, then submit (submit re-enforces mandatory).
    rfq.insert(ignore_permissions=True, ignore_mandatory=True)

    # Link the new RFQ back to the MR (use db_set so we don't trip the
    # workflow's allow-edit / submit guards on the MR).
    mr.db_set("rsb_request_for_quotation", rfq.name)

    return rfq.name
