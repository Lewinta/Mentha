import frappe
from frappe.utils import flt
import json

def on_submit(doc, event):
	update_po_qty_billed(doc, event)

def on_cancel(doc, event):
	update_po_qty_billed(doc, event)

def update_po_qty_billed(doc, event):
	for row in doc.items:
		update_row_qty_billed(row)

def update_row_qty_billed(row):
	if not row or not row.po_detail:
		return

	poi = frappe.db.sql("""
		SELECT
			SUM(stock_qty) as stock_qty
		FROM
			`tabPurchase Invoice Item`
		WHERE
			`tabPurchase Invoice Item`.docstatus = 1
		AND
			`tabPurchase Invoice Item`.item_code = %s
		AND
			`tabPurchase Invoice Item`.po_detail = %s
		GROUP BY
			`tabPurchase Invoice Item`.purchase_order
	""", (row.item_code, row.po_detail), debug=False, as_list=True)
	
	stock_qty = poi[0][0] if poi else 0
	
	frappe.db.set_value("Purchase Order Item", row.po_detail, "billed_qty", stock_qty)

	# Now let's update the Bill Qty on the PO

	po = frappe.db.sql("""
		SELECT
			SUM(stock_qty) as stock_qty,
			SUM(billed_qty) as billed_qty
		FROM
			`tabPurchase Order Item`
		WHERE
			`tabPurchase Order Item`.docstatus = 1
		AND
			`tabPurchase Order Item`.parent = %s
		GROUP BY
			`tabPurchase Order Item`.parent

	""", row.purchase_order, debug=False)
	
	stock_qty, billed_qty = po[0] if po else 0
	per_qty_billed = flt(billed_qty) / flt(stock_qty) * 100
	frappe.db.set_value("Purchase Order", row.purchase_order, "qty_billed", billed_qty)
	frappe.db.set_value("Purchase Order", row.purchase_order, "per_qty_billed", flt(per_qty_billed, 2))

@frappe.whitelist()
def get_po_info(items):
	if type(items) == unicode:
		items = json.loads(
			items.replace("u'", "'").replace("'", "\"")
		)
	for item in items:
		if not item.get("purchase_order"):
			continue

		po_type = frappe.db.get_value(
			"Purchase Order",
			item.get("purchase_order"),
			"order_type"
		)

		if po_type == "TEL VAYDA":
			item.update({
				"rate": .000,
				"amount": .000
			})
	return items




