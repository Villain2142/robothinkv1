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

class ClassRecords(Document):
	def validate(self):
		self.validate_code()
	@frappe.whitelist()
	def validate_code(self):
		if self.courses:
			courses_doc = frappe.get_doc("Courses",self.courses)
			if courses_doc.content:
				if not self.lessons:
					for x in courses_doc.content:
						self.append("lessons",{
							"lesson_no": x.lesson_no,
							"lesson": x.lesson,
							"content_type": x.content_type,
							"lesson_focus": x.lesson_focus,
							"description": x.description
						})
					frappe.db.commit()
			else:
				frappe.msgprint("There is current Lessons in Courses Please check")
		if self.date_wise:
			curret_doc =  self.date_wise[-1]
			if not curret_doc.lesson:
				if self.lessons:
					upcoming_doc = self.lessons[0]
					curret_doc.lesson = upcoming_doc.lesson
					self.lessons.remove(upcoming_doc)
					frappe.db.commit()
					
	@frappe.whitelist()
	def fetch_lessons(self):
		if self.courses:
			courses_doc = frappe.get_doc("Courses",self.courses)
			if courses_doc.content:
				for x in courses_doc.content:
					self.append("lessons",{
						"lesson_no": x.lesson_no,
						"lesson": x.lesson,
						"content_type": x.content_type,
						"lesson_focus": x.lesson_focus,
						"description": x.description
					})
				self.save()
				self.reload()
				frappe.db.commit()
			else:
				frappe.msgprint("There is current Lessons in Courses Please check")

	@frappe.whitelist()
	def end_timer(self):
		if self.start_time:
			self.start_time = ""
			# for x in self.date_wise[:-1]:
			x  = self.date_wise[-1]
			if x.lesson and x.difficulty_level and x.engagement_level and x.lesson_completion_speed and x.image_description:
				x.check_out = frappe.utils.get_datetime()
			else:
				frappe.throw("Please Add Lesson / Feedback")
			self.status = "Out"
			self.save()
			self.reload()
	# def before_submit(self):
	# 	self.invoice_submission()
	# 	self.customer_details_update()
