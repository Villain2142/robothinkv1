# Copyright (c) 2021, tarunsairam2142 and contributors
# For license information, please see license.txt

# import frappe
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

class CoursesType(Document):
	pass
	# def validate(self):
	# 	self.brand_validation()

	# def brand_validation(self):

	# 	if not frappe.db.exists("Brand",self.brand):
	# 		brand_doc = frappe.new_doc("Brand")
	# 		brand_doc.brand = self.course_name
	# 		brand_doc.insert()
	# 		self.brand = brand_doc.name
	# 	else:
	# 		brand_doc = frappe.get_doc("Brand",self.brand)
	# 		self.brand = brand_doc.name
	# 		frappe.db.commit()