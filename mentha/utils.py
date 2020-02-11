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