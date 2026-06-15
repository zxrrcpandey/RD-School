// Copyright (c) 2026, Trustbit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Gate Entry", {
	onload(frm) {
		if (frm.is_new() && !frm.doc.company) {
			frm.set_value("company", frappe.defaults.get_user_default("company"));
		}
	},
	refresh(frm) {
		if (frm.is_new()) return;

		// No actions on terminal statuses — keeps stale buttons from showing.
		if (["Closed - Paid", "Closed - Direct", "Cancelled"].includes(frm.doc.status)) {
			return;
		}

		// Route A: PO Inward
		if (frm.doc.inward_type === "PO Inward") {
			if (frm.doc.status === "At Gate") {
				frm.add_custom_button(__("Route to Store"), () => {
					frm.call({ doc: frm.doc, method: "route_to_store" }).then(() => frm.reload_doc());
				});
			}
			if (frm.doc.status === "Routed to Store" && !frm.doc.linked_purchase_receipt) {
				frm.add_custom_button(__("Purchase Receipt"), () => {
					frm.call({ doc: frm.doc, method: "make_purchase_receipt" }).then((r) => {
						if (r.message) {
							frappe.model.sync(r.message);
							frappe.set_route("Form", r.message.doctype, r.message.name);
						}
					});
				}, __("Create"));
			}
		}

		// Route B: Direct Inward. The gate user only HANDS OFF to reception —
		// they are not routed to the Direct Inward Receipt form (that's the
		// Reception user's screen). Stay on the Gate Entry and show a confirmation.
		if (frm.doc.inward_type === "Direct Inward") {
			if (frm.doc.status === "At Gate") {
				frm.add_custom_button(__("Send to Reception"), () => {
					frm.call({ doc: frm.doc, method: "make_direct_inward" }).then((r) => {
						if (r.message) {
							frappe.show_alert({
								message: __("Sent to Reception ({0}). Reception will route it to the department.", [r.message]),
								indicator: "green",
							});
							frm.reload_doc();
						}
					});
				});
			}
			// Once handed off, give a passive link to view the receipt (read-only
			// reference) — but do not auto-navigate the gate user there.
			if (frm.doc.linked_direct_inward) {
				frm.add_custom_button(
					__("View Direct Inward Receipt"),
					() => frappe.set_route("Form", "Direct Inward Receipt", frm.doc.linked_direct_inward),
					__("View")
				);
			}
		}

		// Cancel (only before any downstream record)
		if (frm.doc.status === "At Gate") {
			frm.add_custom_button(__("Cancel Entry"), () => {
				frm.call({ doc: frm.doc, method: "cancel_entry" }).then(() => frm.reload_doc());
			});
		}
	},
});
