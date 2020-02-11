frappe.ui.form.on("Purchase Receipt", {
	refresh: frm => {
		frm.trigger("set_read_only_fields");
	},
	set_read_only_fields: (frm,) => {
		if (!frm.doc.items)
			return
		if (!frm.doc.items[0].purchase_order)
			return
		
		
	}
});

