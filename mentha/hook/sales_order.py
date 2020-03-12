import frappe

def validate(doc, event):
	pass
	# check_over_delivery(doc)

@frappe.whitelist()
def check_over_delivery(customer):
	results = get_over_delivery(customer)
	if not results:
		return 
	row = results[0]
	msg =  """<b>{customer}</b> has an over-delivery amount 
		of <b>{pending} {item_code}</b> on:<br> <b>
		<a href='/desk#Form/Delivery Note/{parent}' target='_blank'>{parent}</a>.</b><br> 
		Please create a sales invoice for this customer """.format(**row)
	return {"row": row, "msg": msg}

def get_over_delivery(customer): 
	# This will look for any delivery note detail that hasn't been 
	# billed completely and warn the user

	return frappe.db.sql("""
		SELECT
			`tabDelivery Note`.customer,
			`tabDelivery Note Item`.name,
			`tabDelivery Note Item`.parent,
			`tabDelivery Note Item`.item_code,
			`tabDelivery Note Item`.item_name,
			(`tabDelivery Note Item`.stock_qty - `tabDelivery Note Item`.billed_qty) as pending
		FROM 
			`tabDelivery Note Item`
		JOIN
			`tabDelivery Note`
		ON
			`tabDelivery Note`.name = `tabDelivery Note Item`.parent
		AND
			`tabDelivery Note`.docstatus = 1
		WHERE
			`tabDelivery Note`.customer = %s
		AND
			ISNULL(`tabDelivery Note Item`.so_detail)
		HAVING 
			pending > 0
	""", customer, debug=False, as_dict=True)

@frappe.whitelist()
def create_over_delivery_inv(customer):
	import json
	results = get_over_delivery(customer)
	
	if not results:
		return
	
	row = results[0]
	sinv = frappe.new_doc("Sales Invoice")
	sinv.update({
		"customer": row.customer,
	})
	
	sinv.append("items", {
		"dn_detail": row.name,
		"delivery_note": row.parent,
		"item_code": row.item_code,
		"qty": row.pending,
	})

	sinv.set_missing_values()
	sinv.save()
	frappe.db.commit()
	return sinv.name
	



