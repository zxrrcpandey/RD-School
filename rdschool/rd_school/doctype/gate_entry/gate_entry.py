# Copyright (c) 2026, Trustbit and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class GateEntry(Document):
	def validate(self):
		if not self.company:
			self.company = frappe.defaults.get_global_default("company")
		if (self.number_of_packages or 0) < 1:
			frappe.throw(_("Number of packages must be at least 1."))
		# If a Supplier master is linked but the free-text party name is blank,
		# copy it across (keeps the 2-field gate form quick).
		if self.supplier and not self.party_name:
			self.party_name = frappe.db.get_value("Supplier", self.supplier, "supplier_name")

		if self.inward_type == "PO Inward":
			if not self.purchase_order:
				frappe.throw(_("Select the Purchase Order for a PO Inward."))
			po_company = frappe.db.get_value("Purchase Order", self.purchase_order, "company")
			if po_company and self.company and po_company != self.company:
				frappe.throw(_("Purchase Order belongs to a different company."))
		elif self.inward_type == "Direct Inward":
			if not self.destination_department:
				frappe.throw(_("Select the Destination Department for a Direct Inward."))

		# Once the entry has left the gate (status advanced) it is a locked
		# record — block edits to the consignment/routing fields so it can't be
		# altered after a PR/PI or department routing has happened.
		if not self.is_new() and self.status not in ("At Gate",):
			before = self.get_doc_before_save()
			if before:
				locked = [
					"inward_type", "number_of_packages", "package_type",
					"party_name", "supplier", "purchase_order",
					"destination_department", "vehicle_no",
				]
				changed = [
					f for f in locked if (self.get(f) or "") != (before.get(f) or "")
				]
				if changed:
					frappe.throw(
						_("This Gate Entry has advanced (status: {0}) and can no "
						  "longer be edited. Changed: {1}").format(
							self.status, ", ".join(changed)
						)
					)

	@frappe.whitelist()
	def route_to_store(self):
		"""Route A step A1 — advance to Routed to Store (manual; gate operator)."""
		if self.inward_type != "PO Inward":
			frappe.throw(_("Route to Store applies to PO Inward only."))
		self.db_set("status", "Routed to Store")
		_notify_role(
			"School Stores Incharge", self,
			f"Gate Entry {self.name}: consignment routed to Store",
			f"<p>Consignment <b>{self.name}</b> ({self.number_of_packages} "
			f"{self.package_type}) from {self.party_name} against PO "
			f"{self.purchase_order} is at the store. Create the Purchase "
			f"Receipt (GRN) to record it.</p>",
		)
		return self.status

	@frappe.whitelist()
	def make_purchase_receipt(self):
		"""Route A step A2 — create a Purchase Receipt prefilled from the PO."""
		if self.inward_type != "PO Inward":
			frappe.throw(_("Purchase Receipt can only be created for PO Inward entries."))
		if not self.purchase_order:
			frappe.throw(_("No Purchase Order linked."))
		if self.linked_purchase_receipt:
			frappe.throw(_("A Purchase Receipt {0} is already linked.").format(self.linked_purchase_receipt))
		from erpnext.buying.doctype.purchase_order.purchase_order import (
			make_purchase_receipt as _mpr,
		)

		pr = _mpr(self.purchase_order)
		pr.gate_entry = self.name  # custom field on Purchase Receipt
		return pr  # returned to the client; Stores reviews & submits

	@frappe.whitelist()
	def make_direct_inward(self):
		"""Route B step B1 — spawn a Direct Inward Receipt for reception."""
		if self.inward_type != "Direct Inward":
			frappe.throw(_("Direct Inward applies to Direct Inward entries only."))
		if self.linked_direct_inward:
			frappe.throw(_("A Direct Inward Receipt {0} already exists.").format(self.linked_direct_inward))
		dir_doc = frappe.get_doc(
			{
				"doctype": "Direct Inward Receipt",
				"company": self.company,
				"gate_entry": self.name,
				"party_name": self.party_name,
				"number_of_packages": self.number_of_packages,
				"package_type": self.package_type,
				"destination_department": self.destination_department,
				"status": "At Reception",
			}
		)
		dir_doc.insert(ignore_permissions=True)
		self.db_set("linked_direct_inward", dir_doc.name)
		self.db_set("status", "Sent to Reception")
		# Notify Reception against the Direct Inward Receipt (NOT the Gate
		# Entry) so clicking the bell alert opens the receipt they must action.
		_notify_role(
			"School Reception", dir_doc,
			f"Parcel at reception — {dir_doc.name}",
			f"<p>A direct delivery ({self.number_of_packages} {self.package_type}) "
			f"from {self.party_name} for department "
			f"{self.destination_department} is at reception. Open this receipt "
			f"and click <b>Notify Department</b>.</p>",
		)
		return dir_doc.name

	@frappe.whitelist()
	def cancel_entry(self):
		if self.linked_purchase_receipt or self.linked_direct_inward:
			frappe.throw(_("Cannot cancel — a downstream record is already linked."))
		self.db_set("status", "Cancelled")
		return self.status


def _notify_role(role, doc, subject, message):
	"""Insert a System Notification (bell) Notification Log row for every user
	holding `role`. No SMTP needed."""
	for user in _users_with_role(role):
		_insert_notification_log(user, doc, subject, message)


def _users_with_role(role):
	users = frappe.db.sql_list(
		"""
		select distinct hr.parent
		from `tabHas Role` hr
		join `tabUser` u on u.name = hr.parent
		where hr.role = %s and u.enabled = 1 and u.user_type = 'System User'
		""",
		role,
	)
	return [u for u in users if u not in ("Administrator", "Guest")]


def _insert_notification_log(user, doc, subject, message):
	if not user:
		return
	frappe.get_doc(
		{
			"doctype": "Notification Log",
			"for_user": user,
			"type": "Alert",
			"document_type": doc.doctype,
			"document_name": doc.name,
			"subject": subject,
			"email_content": message,
		}
	).insert(ignore_permissions=True)
