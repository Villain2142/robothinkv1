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

class Franchise(Document):
	def validate(self):
		self.make_company()
		self.item_group()
		self.postcode_validations()
	def make_company(self):
		c_name =  str(self.name1)
		if not frappe.db.exists("Company",self.company):
			company = frappe.new_doc("Company")
			company.company_name = self.company
			company.default_currency = "GBP"
			company.country = "United Kingdom"
			company.abbr = self.name1
			company.franchises = self.name1
			company.franchise_id = self.name
			company.insert()
			self.company = company.name
		else:
			company_doc = frappe.get_doc("Company",self.company)
			if company_doc.franchises != self.name1:
				company_doc.franchises = self.name1
				company_doc.franchise_id = self.name
				company_doc.save()
	def item_group(self):
		if not frappe.db.exists("Item Group",self.item_group_id):
			igroup = frappe.new_doc("Item Group")
			igroup.item_group_name = self.name1
			igroup.show_in_website = 1
			igroup.Title = self.name1
			igroup.insert()
			self.item_group_id = igroup.name
		else:
			item_group_doc = frappe.get_doc("Item Group",self.item_group_id)
			self.item_group_id = item_group_doc.name
			frappe.db.commit()

	def postcode_validations(self):
		if self.locations:
			new_list = []
			old_list = []
			for postcode in self.locations:
				# if not frappe.db.exists("Postcode",postcode.postcode):
				# 	n_postcode = frappe.new_doc("Postcode")
				# 	n_postcode.postcode = postcode.postcode
				# 	n_postcode.franchise = self.name
				# 	n_postcode.insert("ignore_permissions")
				# 	new_list.append(n_postcode.name)
				n_postcode = frappe.get_doc("Postcode",postcode.postcode)
				if not n_postcode.franchise:
					n_postcode.franchise = self.name
					n_postcode.save("ignore_permissions")
				if n_postcode.franchise != self.name:
					old_list.append(n_postcode.name)
			if len(old_list):
				frappe.throw(_("Postcode is not valid {0}").format(old_list))