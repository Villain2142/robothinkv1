# Copyright (c) 2021, tarunsairam2142 and contributors
# For license information, please see license.txt

import re
from time import sleep
from bs4 import element
import frappe
from frappe.model.document import Document
from frappe.contacts.doctype.address.address import get_address_display
from frappe.utils import esc, flt, cint, nowdate
from frappe.utils.data import today

from erpnext.controllers.accounts_controller import get_taxes_and_charges
from frappe import throw, _
import frappe.defaults
from frappe.utils import getdate
from erpnext.controllers.buying_controller import BuyingController
from erpnext.accounts.utils import get_account_currency
from frappe.desk.notifications import clear_doctype_notifications
from frappe.model.mapper import get_mapped_doc
from erpnext.buying.utils import check_on_hold_or_closed_status
from erpnext.assets.doctype.asset.asset import get_asset_account, is_cwip_accounting_enabled
from erpnext.assets.doctype.asset_category.asset_category import get_asset_category_account
from frappe.utils.data import format_duration
from six import iteritems
from erpnext.stock.doctype.delivery_note.delivery_note import make_inter_company_transaction
from erpnext.accounts.doctype.payment_request.payment_request import make_payment_request, make_payment_entry

class ScheduledClass(Document):
	def validate(self):
		self.item_validation()

	def item_validation(self):
		if not frappe.db.exists("Item",self.item):
			course_doc = frappe.get_doc("Courses",self.course_name)
			item_doc = frappe.new_doc("Item")
			item_doc.item_code = self.name
			item_doc.item_name = self.course_name
			item_doc.item_group = self.franchise
			item_doc.stock_uom = self.session_type
			item_doc.standard_rate = self.per_session_cost
			item_doc.courses = self.course_name
			item_doc.category = self.category
			item_doc.courses_type = self.courses_type
			item_doc.has_batch_no = 1
			item_doc.is_sales_item = 1
			item_doc.show_in_website = 1
			item_doc.website_warehouse = self.venue
			item_doc.web_long_description = course_doc.description
			item_doc.website_specifications = course_doc.website_specifications
			item_doc.insert()
			self.item = item_doc.name
		else:
			item_doc = frappe.get_doc("Brand",self.item)
			self.item = item_doc.name
			frappe.db.commit()
