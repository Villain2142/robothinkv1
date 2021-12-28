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

class Instructors(Document):
	def validate(self):
		pass
		# self.validate_duplicate_employee()

	def validate_duplicate_employee(self):
		if self.employee and frappe.db.get_value("Instructors", {'employee': self.employee, 'name': ['!=', self.name]}, 'name'):
			frappe.throw(_("Employee ID is linked with another instructor"))
	@frappe.whitelist()
	def start_timer(self):
		if self.employee and self.shift:
			print(today(),"bsdkbdskvbksvbskvbskvbskvbskhvb           ,.,kj")
			if not self.start_time:
				self.start_time = frappe.utils.get_datetime()
				attendance_doc = frappe.new_doc("Attendance")
				attendance_doc.employee = self.employee
				attendance_doc.status = "Present"
				attendance_doc.attendance_date = today()
				attendance_doc.shift = self.shift
				attendance_doc.in_time = self.start_time
				attendance_doc.save()
				self.status = "Active"
				self.save()
				self.reload()
			else:
				if frappe.db.exists("Attendance",{"employee":self.employee,"attendance_date":today()}):
					attendance_doc = frappe.get_doc("Attendance",{"employee":self.attendance_date,"in_time":today()})
					attendance_doc.status =  "Present"
					attendance_doc.attendance_date = today()
					attendance_doc.shift = self.shift
					attendance_doc.in_time = self.start_time
					attendance_doc.save()
				else:
					attendance_doc = frappe.new_doc("Attendance")
					attendance_doc.employee = self.employee
					attendance_doc.status = "Present"
					attendance_doc.attendance_date = today()
					attendance_doc.shift = self.shift
					attendance_doc.in_time = self.start_time
					attendance_doc.save()
					
				self.status = "Active"
				self.save()
				self.reload()
		else:
			frappe.throw("Please Add Employee and Shift Details for tracking")
	@frappe.whitelist()
	def end_timer(self):
		if self.start_time:
			print(self.start_time,"check data time")
			if frappe.db.exists("Attendance",{"employee":self.employee,"attendance_date":today()}):
				attendance_doc = frappe.get_doc("Attendance",{"employee":self.employee,"attendance_date":today()})
				attendance_doc.out_time = frappe.utils.get_datetime()
				attendance_doc.save()
				attendance_doc.submit()
				self.status = "In Active"
				self.save()
				self.reload()
			else:
				frappe.throw("No Record Found")
			self.status = "In Active"
			self.start_time = ""
			self.end_time = ""
			self.save()
			self.reload()