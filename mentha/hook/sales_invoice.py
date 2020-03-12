import frappe

def on_submit(doc, event):
	update_billed_qty_dn(doc)

def on_cancel(doc, event):
	update_billed_qty_dn(doc, True)
	

def update_billed_qty_dn(doc, cancel=False):
	for item in doc.items:
		if not item.delivery_note:
			continue

		dn = frappe.get_doc("Delivery Note", item.delivery_note)
		match = filter(lambda x, dn_detail=item.dn_detail : x.get('name') == dn_detail, dn.items)
		if not match:
			continue
		match = match[0]
		
		if cancel:
			match.billed_qty -= item.stock_qty
		else:
			match.billed_qty += item.stock_qty

		# Now you need to ask him how to calculate billed qty for the DN
		# And what would happen with the other items 
		match.db_update()
		frappe.db.commit()

	total_qty  = .00
	billed_qty = .00

	for item in dn.items:
		total_qty  += item.stock_qty
		billed_qty += item.billed_qty

	dn.per_qty_billed = (billed_qty / total_qty) * 100.00
	dn.db_update()
	frappe.db.commit()