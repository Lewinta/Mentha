frappe.ui.form.on("Purchase Invoice", {
	validate: frm => {
		frm.trigger("validate_rates");
	},
	validate_rates: frm => {
		$.map(frm.doc.items, item => {
			if (item.rate == 0.00){
				frappe.throw("Rate on line " + item.idx + " must be greather than 0!");
				validated = false;
			}
		});
			
	},
	onload_post_render: frm => {
		if(!frm.doc.is_new())
			return
		frm.trigger("check_order_type");
	},
	check_order_type: frm => {
		if (!frm.doc.items)
			return

		let opts = {
			"method": "mentha.hook.purchase_invoice.get_po_info"
		};

		opts.args = { "items": frm.doc.items };

		// ok, now we're ready to send the request
		frappe.call(opts).then((response) => {
			// set the response body to a local variable
			let items = response.message;
			if (items){
				$.map(items, ({doctype, name, rate}) => {
					console.log(doctype + " - " + name + "-" + rate);

					frappe.model.set_value(doctype, name, "rate", rate);
				});
				frm.fields_dict.items.grid.fields_map.rate.reqd = 1;
				frm.fields_dict.items.grid.fields_map.amount.reqd = 1;
			}
		}, (exec) => frappe.msgprint("¡There was a problem getting order type!"));
	}
});

