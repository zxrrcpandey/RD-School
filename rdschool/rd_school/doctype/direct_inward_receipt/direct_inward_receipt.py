# Copyright (c) 2026, Trustbit and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime

from rdschool.rd_school.doctype.gate_entry.gate_entry import _insert_notification_log


class DirectInwardReceipt(Document):
	def validate(self):
		if not self.company:
			self.company = frappe.defaults.get_global_default("company")

	@frappe.whitelist()
	def notify_department(self):
		"""Route B step B2 — Reception routes to the department and pings the
		department contact(s). Targets the department's notify-users list
		(custom field rsb_notify_users), falling back to all School HOD users.
		"""
		if not self.destination_department:
			frappe.throw(_("Choose a Destination Department first."))
		self.db_set("status", "Awaiting Department")

		recipients = _department_recipients(self.destination_department)
		subject = f"Delivery for your department — {self.name}"
		message = (
			f"<p>A delivery has arrived for <b>{self.destination_department}</b>:</p>"
			f"<p>{self.number_of_packages} {self.package_type} from "
			f"{self.party_name}.<br>{self.item_description or ''}</p>"
			f"<p>Open <b>{self.name}</b> and click <b>Acknowledge Receipt</b> "
			f"once you have collected it.</p>"
		)
		for user in recipients:
			_insert_notification_log(user, self, subject, message)
		if not recipients:
			frappe.msgprint(
				_("No department contact configured — set 'Notify Users' on the "
				  "Department, or notify the recipient manually.")
			)
		return {"status": self.status, "notified": recipients}

	@frappe.whitelist()
	def acknowledge_receipt(self, remarks=None):
		"""Route B step B3/B4 — the department end-user signs off; auto-closes
		this record and the parent Gate Entry."""
		self.received_by = frappe.session.user
		self.received_on = now_datetime()
		if remarks:
			self.acknowledgment_remarks = remarks
		self.status = "Closed - Received"
		self.save(ignore_permissions=True)
		# Propagate closure back to the parent Gate Entry.
		if self.gate_entry:
			frappe.db.set_value("Gate Entry", self.gate_entry, "status", "Closed - Direct")
		return self.status

	@frappe.whitelist()
	def cancel_receipt(self):
		self.db_set("status", "Cancelled")
		return self.status


def _department_recipients(department):
	"""Users to notify for a department. Primary: the department's custom
	'rsb_department_incharge' (Link User) field set by admin. Fallback: all
	School HOD users (coarse — refine by setting the in-charge per department).
	"""
	recipients = []
	meta = frappe.get_meta("Department")
	if meta.has_field("rsb_department_incharge"):
		incharge = frappe.db.get_value("Department", department, "rsb_department_incharge")
		if incharge:
			recipients = [incharge]
	if not recipients:
		from rdschool.rd_school.doctype.gate_entry.gate_entry import _users_with_role
		recipients = _users_with_role("School HOD")
	# de-dup, drop system users
	seen, out = set(), []
	for u in recipients:
		if u and u not in seen and u not in ("Administrator", "Guest"):
			seen.add(u)
			out.append(u)
	return out
