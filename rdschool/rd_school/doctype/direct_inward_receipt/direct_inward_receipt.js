// Copyright (c) 2026, Trustbit and contributors
// For license information, please see license.txt

frappe.ui.form.on("Direct Inward Receipt", {
	refresh(frm) {
		if (frm.is_new()) return;

		// B2 — Reception routes to the department and notifies them.
		if (frm.doc.status === "At Reception") {
			frm.add_custom_button(__("Notify Department"), () => {
				frm.call({ doc: frm.doc, method: "notify_department" }).then(() => frm.reload_doc());
			}).addClass("btn-primary");
		}

		// B3/B4 — the department end-user acknowledges receipt.
		if (frm.doc.status === "Awaiting Department") {
			frm.add_custom_button(__("Acknowledge Receipt"), () => {
				frappe.prompt(
					[{ fieldname: "remarks", fieldtype: "Small Text", label: __("Remarks (optional)") }],
					(values) => {
						frm.call({
							doc: frm.doc,
							method: "acknowledge_receipt",
							args: { remarks: values.remarks },
						}).then(() => frm.reload_doc());
					},
					__("Acknowledge Receipt"),
					__("Confirm Received")
				);
			}).addClass("btn-primary");
		}

		if (["At Reception", "Awaiting Department"].includes(frm.doc.status)) {
			frm.add_custom_button(__("Cancel"), () => {
				frm.call({ doc: frm.doc, method: "cancel_receipt" }).then(() => frm.reload_doc());
			});
		}
	},
});
