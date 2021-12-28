# Copyright (c) 2021, tarunsairam2142 and contributors
# For license information, please see license.txt

from math import e
import re
from time import sleep
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

class CampAttendance(Document):
	def validate(self):
		self.validate_code()
	@frappe.whitelist()
	def validate_code(self):
		if self.parent_id:
			parent_doc = frappe.get_doc("Parents",self.parent_id)
			print("Image is loding up",parent_doc.image)
			self.parent_image_file = parent_doc.image
		if self.child_id:
			child_doc = frappe.get_doc("Child Info",self.child_id)
			self.child_image_file = child_doc.image
	@frappe.whitelist()
	def vlidate_parents_code(self):
		if self.parent_id:
			parent_doc = frappe.get_doc("Parents",self.parent_id)
			print("Image is loding up",parent_doc.image)
			self.parent_image_file = parent_doc.image
		if self.child_id:
			child_doc = frappe.get_doc("Child Info",self.child_id)
			self.child_image_file = child_doc.image
		self.save()
	@frappe.whitelist()
	def select_company(self):

		user = frappe.session.user
		company = frappe.get_value('Employee',{'user_id': user}, 'company')
		print("cyess calling",user)
		return company
	@frappe.whitelist()
	def child_records_update(self):
		self.append("check_in_records", {
			"parent_name":self.parent_name,
			"child_id": self.child_id,
			"facility": self.facility,
			"instructors": self.instructors,
			"check_in_time": frappe.utils.get_datetime(),
			"duration" : 90,
		})
		frappe.msgprint("Class Record Created")
		self.child_id = ""
		self.parent_id = ""
		self.child_name = ""
		self.parent_name = ""
		self.save()
		self.reload()
		return True


	# def before_submit(self):
	# 	self.invoice_submission()
	# 	self.customer_details_update()

