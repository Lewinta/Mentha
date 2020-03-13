import frappe

@frappe.whitelist()
def get_last_purchase_rate(item_code):
	rate_map = frappe.db.sql("""
		SELECT * FROM (
			SELECT
				result.item_code,
				result.base_rate
			FROM (
					(SELECT
						po_item.item_code,
						po_item.item_name,
						po.transaction_date AS posting_date,
						po_item.base_price_list_rate,
						po_item.discount_percentage,
						po_item.base_rate
					FROM `tabPurchase Order` po, `tabPurchase Order Item` po_item
					WHERE po.name = po_item.parent AND po.docstatus = 1
				)
			UNION
				(
					SELECT
						pr_item.item_code,
						pr_item.item_name,
						pr.posting_date,
						pr_item.base_price_list_rate,
						pr_item.discount_percentage,
						pr_item.base_rate
					FROM `tabPurchase Receipt` pr, `tabPurchase Receipt Item` pr_item
					WHERE pr.name = pr_item.parent AND pr.docstatus = 1
				)
		) result
		ORDER BY result.item_code ASC, result.posting_date DESC) result_wrapper
		GROUP BY item_code""",
		as_dict=True
	)

	price = filter(lambda x, item_code=item_code: x.item_code == item_code, rate_map)  

	return price[0].base_rate if price else 0.00
def update_po_billed_qty():
	frappe.db.sql("""
		UPDATE
			`tabPurchase Order Item`
		JOIN
			`tabPurchase Order`
		ON
			`tabPurchase Order`.name = `tabPurchase Order Item`.parent
		SET 
			`tabPurchase Order Item`.billed_qty = `tabPurchase Order Item`.received_qty
		WHERE
			`tabPurchase Order`.status in ('Completed', 'Closed')
	""")

	print("Purchase Order Item Updated")
	
	frappe.db.sql("""
		CREATE VIEW `viewPO_summary`as SELECT
			`tabPurchase Order`.name,
			`tabPurchase Order`.total_qty,
			SUM(`tabPurchase Order Item`.billed_qty) billed_qty
		FROM
			`tabPurchase Order Item`
		JOIN
			`tabPurchase Order`
		ON
			`tabPurchase Order`.name = `tabPurchase Order Item`.parent
		WHERE
			`tabPurchase Order`.status in ('Completed', 'Closed')
		GROUP BY
			`tabPurchase Order`.name
	""")

	print("View viewPO_summary Created")

	frappe.db.sql("""
		UPDATE
			`tabPurchase Order`
		JOIN
			`viewPO_summary`
		ON
			`tabPurchase Order`.name = `viewPO_summary`.name
		SET 
			`tabPurchase Order`.qty_billed = `viewPO_summary`.billed_qty,
			`tabPurchase Order`.per_qty_billed = (`viewPO_summary`.billed_qty / `tabPurchase Order`.total_qty) * 100
	""")
	print("Purchase Order Updated")

	frappe.db.sql("""DROP VIEW `viewPO_summary`""")

	print("View viewPO_summary Created")
	
def update_dn_billed_qty():
	frappe.db.sql("""
		UPDATE
			`tabDelivery Note Item`
		JOIN
			`tabDelivery Note`
		ON
			`tabDelivery Note`.name = `tabDelivery Note Item`.parent
		SET 
			`tabDelivery Note Item`.billed_qty = `tabDelivery Note Item`.stock_qty
		WHERE
			`tabDelivery Note`.status in ('Completed', 'Closed')
	""")
	print("Delivery note Item updated successfully")

	frappe.db.sql("""
		CREATE VIEW `viewDN_summary`as SELECT
			`tabDelivery Note`.name,
			`tabDelivery Note`.total_qty,
			SUM(`tabDelivery Note Item`.billed_qty) billed_qty
		FROM
			`tabDelivery Note Item`
		JOIN
			`tabDelivery Note`
		ON
			`tabDelivery Note`.name = `tabDelivery Note Item`.parent
		WHERE
			`tabDelivery Note`.status in ('Completed', 'Closed')
		GROUP BY
			`tabDelivery Note`.name
	""")

	print("view created successfully")

	frappe.db.sql("""
		UPDATE
			`tabDelivery Note`
		JOIN
			`viewDN_summary`
		ON
			`tabDelivery Note`.name = `viewDN_summary`.name
		SET 
			`tabDelivery Note`.per_qty_billed = (`viewDN_summary`.billed_qty / `tabDelivery Note`.total_qty) * 100
	""")
	print("Delivery Notes Updated!")

	frappe.db.sql("""
		DROP VIEW `viewDN_summary`
	""")
	print("View Dropped")