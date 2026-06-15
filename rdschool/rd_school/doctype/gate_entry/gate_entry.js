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

		// Route B: Direct Inward
		if (frm.doc.inward_type === "Direct Inward") {
			if (frm.doc.status === "At Gate") {
				frm.add_custom_button(__("Send to Reception"), () => {
					frm.call({ doc: frm.doc, method: "make_direct_inward" }).then((r) => {
						if (r.message) frappe.set_route("Form", "Direct Inward Receipt", r.message);
					});
				});
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
