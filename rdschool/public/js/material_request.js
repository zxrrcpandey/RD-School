// rdschool customizations on the Material Request form.
// Loaded via hooks.py `doctype_js`.

frappe.ui.form.on("Material Request", {
	refresh(frm) {
		// On the out-of-stock branch, give the Store a one-click way to raise
		// the RFQ pre-filled with this MR's items (the native Create→RFQ button
		// is hidden because the MR is still a draft during approval).
		if (
			frm.doc.workflow_state === "RFQ In Progress" &&
			!frm.doc.rsb_request_for_quotation &&
			frappe.user_roles.includes("School Stores Incharge")
		) {
			frm.add_custom_button(
				__("Raise RFQ"),
				() => {
					frappe.call({
						method: "rdschool.material_request.make_rfq_from_mr",
						args: { material_request: frm.doc.name },
						freeze: true,
						freeze_message: __("Creating Request for Quotation…"),
						callback: (r) => {
							if (r.message) {
								frappe.show_alert({
									message: __("RFQ {0} created — add suppliers and submit.", [r.message]),
									indicator: "green",
								});
								frappe.set_route("Form", "Request for Quotation", r.message);
							}
						},
					});
				},
				__("Create")
			);
		}

		// Quick link to the linked RFQ once it exists.
		if (frm.doc.rsb_request_for_quotation) {
			frm.add_custom_button(
				__("View RFQ"),
				() => frappe.set_route("Form", "Request for Quotation", frm.doc.rsb_request_for_quotation),
				__("Create")
			);
		}

		// On an Approved MR with a chosen quotation, create the PO FROM that
		// Supplier Quotation (carries negotiated rates + links PO↔SQ). This is
		// preferred over the native MR→PO button when a quote was selected.
		if (
			frm.doc.workflow_state === "Approved" &&
			frm.doc.rsb_selected_supplier_quotation &&
			(frappe.user_roles.includes("School Stores Incharge") ||
				frappe.user_roles.includes("Purchase Manager"))
		) {
			frm.add_custom_button(
				__("PO from Selected Quotation"),
				() => {
					frappe.call({
						method: "rdschool.material_request.make_po_from_selected_quotation",
						args: { material_request: frm.doc.name },
						freeze: true,
						freeze_message: __("Creating Purchase Order from the quotation…"),
						callback: (r) => {
							if (r.message) {
								frappe.model.sync(r.message);
								frappe.set_route("Form", r.message.doctype, r.message.name);
							}
						},
					});
				},
				__("Create")
			).addClass("btn-primary");
		}
	},
});
