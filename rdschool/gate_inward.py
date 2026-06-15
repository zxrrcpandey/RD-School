"""Auto-advance Gate Entry status as the PO-inward chain progresses.

Wired via doc_events in hooks.py:
  Purchase Receipt.on_submit  -> Gate Entry status = "Receipt Created"
  Purchase Invoice.on_submit  -> Gate Entry status = "Invoiced"
  Payment Entry.on_submit     -> Gate Entry status = "Closed - Paid"

These are status writes (frappe.db.set_value), independent of any workflow.
"""

import frappe

from rdschool.rd_school.doctype.gate_entry.gate_entry import (
	_insert_notification_log,
	_users_with_role,
)


def _advance_gate(gate_entry, status, notify_role=None, subject=None, message=None):
	if not gate_entry or not frappe.db.exists("Gate Entry", gate_entry):
		return
	frappe.db.set_value("Gate Entry", gate_entry, "status", status)
	if notify_role and subject:
		ge = frappe.get_doc("Gate Entry", gate_entry)
		for user in _users_with_role(notify_role):
			_insert_notification_log(user, ge, subject, message or subject)


def purchase_receipt_on_submit(doc, method=None):
	"""A2 done — GRN logged. Advance the linked Gate Entry, record the PR link
	(so the Create-PR button hides), and notify Accounts."""
	gate_entry = doc.get("gate_entry")
	if not gate_entry or not frappe.db.exists("Gate Entry", gate_entry):
		return
	# Authoritative moment to stamp the back-link (PR is named + persisted).
	frappe.db.set_value("Gate Entry", gate_entry, "linked_purchase_receipt", doc.name)
	_advance_gate(
		gate_entry,
		"Receipt Created",
		notify_role="School Accountant",
		subject=f"Gate Entry {gate_entry}: goods received ({doc.name})",
		message=(
			f"<p>Purchase Receipt <b>{doc.name}</b> was submitted for gate entry "
			f"{gate_entry}. Book the Purchase Invoice against it.</p>"
		),
	)


def _gate_entry_from_pr(purchase_receipt):
	if not purchase_receipt:
		return None
	return frappe.db.get_value("Purchase Receipt", purchase_receipt, "gate_entry")


def purchase_invoice_on_submit(doc, method=None):
	"""A3 done — PI booked. Trace PI -> PR -> Gate Entry and advance."""
	seen = set()
	for item in doc.get("items") or []:
		pr = item.get("purchase_receipt")
		if not pr or pr in seen:
			continue
		seen.add(pr)
		gate_entry = _gate_entry_from_pr(pr)
		if gate_entry:
			_advance_gate(
				gate_entry,
				"Invoiced",
				notify_role="School Accountant",
				subject=f"Gate Entry {gate_entry}: invoice booked ({doc.name})",
				message=(
					f"<p>Purchase Invoice <b>{doc.name}</b> booked. Process the "
					f"vendor payment to close gate entry {gate_entry}.</p>"
				),
			)


def payment_entry_on_submit(doc, method=None):
	"""A4 done — vendor paid. Trace Payment -> PI -> PR -> Gate Entry. Close."""
	seen_pi = set()
	for ref in doc.get("references") or []:
		if ref.get("reference_doctype") != "Purchase Invoice":
			continue
		pi = ref.get("reference_name")
		if not pi or pi in seen_pi:
			continue
		seen_pi.add(pi)
		pi_doc = frappe.get_doc("Purchase Invoice", pi)
		for item in pi_doc.get("items") or []:
			gate_entry = _gate_entry_from_pr(item.get("purchase_receipt"))
			if gate_entry:
				_advance_gate(gate_entry, "Closed - Paid")
