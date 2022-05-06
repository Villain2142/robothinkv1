# Copyright (c) 2021, tarunsairam2142 and contributors
# For license information, please see license.txt
import json

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

class Bookings(Document):


	def on_update(self):
		self.validate_code()
	def on_submit(self):
		self.enroll_to_batch()
	@frappe.whitelist()
	def select_company(self):
		user = frappe.session.user
		company = frappe.get_value('Employee',{'user_id': user}, 'company')
		print("cyess calling",user)
		return company
	@frappe.whitelist()
	def validate_code(self):
		if self.child_name:
			child_doc=  frappe.get_doc("Child Info",self.child_name)
			child_doc.booking_id = self.name
			child_doc.save()
		if self.paid_amount ==0:
			self.due_amount = self.amount
		if self.status == "Active":
			if self.total_active_tokens == 0:
				if self.available_tokens != 0:
					self.total_active_tokens = 1
					self.available_tokens -= 1
					frappe.db.commit()
	@frappe.whitelist()
	def enroll_to_batch(self):
		if self.batches:
			batch_doc = frappe.get_doc("Batches",self.batches)
			batch_doc.append("enrolled_students",{
				"child": self.child_name,
				"booking_info": self.name,
				"date": self.booking_date
			})
			batch_doc.occupied_seats = float(batch_doc.occupied_seats) + 1
			batch_doc.available_seats = float(batch_doc.no_of_seats) - batch_doc.occupied_seats
			batch_doc.save()
			# if len(batch_doc.enrolled_students)>0:
			# 	child_list = []
			# 	for x in batch_doc.enrolled_students:
			# 		if x.child:
			# 			child_list.append(x.child)
			# 		else:
			# 			child_list.append("None")
			# 	if self.child_name:
			# 		if self.child_name in child_list:
			# 			pass
			# 		else:
			# 			batch_doc.append("enrolled_students",{
			# 				"child": self.child_name,
			# 				"booking_info": self.name,
			# 				"date": self.booking_date
			# 			})
			# 			batch_doc.occupied_seats = float(batch_doc.occupied_seats) + 1
			# 			batch_doc.available_seats = float(batch_doc.no_of_seats) - batch_doc.occupied_seats
			# 			batch_doc.save()
			# else:
			# 	batch_doc.append("enrolled_students",{
			# 		"child": self.child_name,
			# 		"booking_info": self.name,
			# 		"date": self.booking_date
			# 	})
			# 	batch_doc.occupied_seats = float(batch_doc.occupied_seats) + 1
			# 	batch_doc.available_seats = float(batch_doc.no_of_seats) - batch_doc.occupied_seats
			# 	batch_doc.save()

	@frappe.whitelist()
	def make_payment(data):
		data = frappe._dict(json.loads(data))
		cond = []
		return True
