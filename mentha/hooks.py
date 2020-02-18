# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "mentha"
app_title = "Mentha"
app_publisher = "Lewin Villar"
app_description = "Customizations on ERPNext"
app_icon = "fa fa-first-order"
app_color = "green"
app_email = "lewin.villar@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mentha/css/mentha.css"
# app_include_js = "/assets/mentha/js/mentha.js"

# include js, css files in header of web template
# web_include_css = "/assets/mentha/css/mentha.css"
# web_include_js = "/assets/mentha/js/mentha.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Purchase Receipt" : "public/js/purchase_receipt.js",
	"Purchase Order" : "public/js/purchase_order.js",
	"Purchase Invoice" : "public/js/purchase_invoice.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}


# Fixtures
# ----------

fixtures = [
	{
		"doctype": "Custom Field",
		"filters": {
			"name": (
				"in", (
					"Purchase Order Item-billed_qty",
					"Purchase Order-qty_billed",
					"Purchase Order-per_qty_billed",
					"Purchase Order-order_type",
				)
			)
		}
	},
]

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "mentha.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

before_install = "mentha.install.before_install"
# after_install = "mentha.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mentha.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Purchase Invoice": {
		"on_submit": "mentha.hook.purchase_invoice.on_submit",
		"on_cancel": "mentha.hook.purchase_invoice.on_cancel",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"mentha.tasks.all"
# 	],
# 	"daily": [
# 		"mentha.tasks.daily"
# 	],
# 	"hourly": [
# 		"mentha.tasks.hourly"
# 	],
# 	"weekly": [
# 		"mentha.tasks.weekly"
# 	]
# 	"monthly": [
# 		"mentha.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "mentha.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "mentha.event.get_events"
# }

