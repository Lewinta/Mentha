frappe.ui.form.on("Sales Order", {
	refresh: frm => {
	},
	validate: frm => {
		let opts = {
			"method": "mentha.hook.sales_order.check_over_delivery",
			"args": { "customer": frm.doc.customer }
		};

		// ok, now we're ready to send the request
		frappe.call(opts).then((response) => {
			// set the response body to a local variable
			if (!response.message)
				return
			let {msg, row} = response.message;
			let _cb = function () {
				frm.doc.row = row;
				frm.trigger("create_invoice");
			}
			if (msg){
				frappe.prompt(
					[{'fieldtype': 'HTML', 'options': `${msg}`}],
					_cb,
					"Over-Delivery Warning",
					"Create Invoice"
				);
				frappe.validated = false;
			}
		}, (exec) => frappe.msgprint("¡There was a problem getting over-delivery info!"));
	},
	create_invoice: frm => {
		frappe.dom.freeze("Creating Invoice");
		let opts = {
			"method": "mentha.hook.sales_order.create_over_delivery_inv",
			"args": { "customer": frm.doc.customer }
		}
		frappe.call(opts).then((response) => {
			let sinv = response.message
			if (sinv){
				frappe.run_serially([
					() => frappe.set_route("Form", "Sales Invoice", sinv),
					() => frappe.dom.unfreeze()
				])
			}
		},(exec) => frappe.msgprint("¡There was a problem getting over-delivery info!"));
	}
})