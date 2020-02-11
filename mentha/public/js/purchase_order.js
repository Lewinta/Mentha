frappe.ui.form.on("Purchase Order", {
	refresh: frm => {

	},
	order_type: frm => {
		const {order_type} = frm.doc;
		let cond = eval(order_type == "TEL VAYDA");
		if (!order_type)
			return
		//Let's set read only the following fields [rate, amount]
		frappe.run_serially([
			() => frm.clear_table("items"),
			() => frm.add_child("items", {}),
			() => frm.fields_dict.items.grid.fields_map.rate.read_only = cond,
			() => frm.refresh_field("items"),
		]);
	}
});

frappe.ui.form.on("Purchase Order Item", {
	item_code: (frm, dt, dn) => {
		let row = frappe.model.get_doc(dt, dn);

		if (frm.doc.order_type != "TEL VAYDA" || !row.item_code)
			return

		frappe.run_serially([
			() => frappe.timeout(1.5),
			() => frappe.model.set_value(dt, dn, "rate", row.last_purchase_rate),
			() => frappe.model.set_value(dt, dn, "price_list_rate", row.last_purchase_rate),
			() => frappe.model.set_value(dt, dn, "discount_percentage", 0.00),
		]);
	}
});