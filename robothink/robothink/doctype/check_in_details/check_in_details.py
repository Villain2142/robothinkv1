# Copyright (c) 2021, tarunsairam2142 and contributors
# For license information, please see license.txt

# import frappe
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


class CheckInDetails(Document):
	def before_insert(self):
		self.get_enrolled_childs()
	def validate(self):
		self.validate_code()
		self.validate_enrolled_childs()
		self.child_attendance_update()

	@frappe.whitelist()
	def validate_enrolled_childs(self):
		if len(self.check_in_records)>0:
			list_child = []
			for c in self.check_in_records:
				list_child.append(c.child_id)
			if self.batch:
				batch_doc = frappe.get_doc("Batches",self.batch)
				if batch_doc.enrolled_students:
					for child in batch_doc.enrolled_students:
						if child.child not in list_child:
							self.append("check_in_records", {
								"child_id": child.child,
								"facility": self.facility,
							})
		else:
			if self.batch:
				batch_doc = frappe.get_doc("Batches",self.batch)
				if batch_doc.enrolled_students:
					for child in batch_doc.enrolled_students:
    						self.append("check_in_records", {
							"child_id": child.child,
							"facility": self.facility,
						})

	@frappe.whitelist()
	def get_enrolled_childs(self):
		if self.batch:
			batch_doc = frappe.get_doc("Batches",self.batch)
			if batch_doc.enrolled_students:
				for child in batch_doc.enrolled_students:
					self.append("check_in_records", {
						"child_id": child.child,
      					"facility": self.facility,
					})

	@frappe.whitelist()
	def validate_code(self):
		try:
			if not self.saved:
				self.saved = 1
			if self.parent_id:
				parent_doc = frappe.get_doc("Parents",self.parent_id)
				print("Image is loding up",parent_doc.image)
				if parent_doc.image:
					self.parent_image_file = parent_doc.image
			if self.child_id:
				child_doc = frappe.get_doc("Child Info",self.child_id)
				if child_doc.image:
					self.child_image_file = child_doc.image
		except Exception as e:
			print (e)
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
	def child_attendance_update(self):
		if self.check_in_records:
			for record in self.check_in_records:
				if not record.check_in_time and record.attendance == "Present":
					booking_id =  frappe.get_doc("Bookings", {"child_name":record.child_id})
					if booking_id.total_active_tokens:
						active_tokens =booking_id.total_active_tokens -1
						used_tokens = booking_id.used_tokens + 1
						booking_id.db_set("total_active_tokens",active_tokens)
						booking_id.db_set("used_tokens",used_tokens)
						self.active_tokens -= 1
					if frappe.db.exists("Program Lobby",{"batch":self.batch ,"date":self.date }):
						p_lobby = frappe.get_doc("Program Lobby",{"batch":self.batch ,"date":self.date })
						p_lobby.append("lobby_child_details", {
							"child": record.child_id,
							"program": self.program,
							"in_time": frappe.utils.get_datetime(),
						})
						p_lobby.save()
					else:
						p_lobby = frappe.new_doc("Program Lobby")
						p_lobby.company = self.company
						p_lobby.franchise = self.franchise
						p_lobby.venue = self.venue
						p_lobby.batch = self.batch
						p_lobby.date = self.date
						p_lobby.append("lobby_child_details", {
							"child": record.child_id,
							"program": self.program,
							"in_time": frappe.utils.get_datetime(),
						})
						p_lobby.save()
					record.check_in_time = frappe.utils.get_datetime()



	@frappe.whitelist()
	def child_records_update(self):
		if self.active_tokens:
			booking_id =  frappe.get_doc("Bookings", {"child_name":self.child_id})
			if booking_id.total_active_tokens:
				active_tokens =booking_id.total_active_tokens -1
				used_tokens = booking_id.used_tokens + 1
				booking_id.db_set("total_active_tokens",active_tokens)
				booking_id.db_set("used_tokens",used_tokens)
				self.active_tokens -= 1
			if frappe.db.exists("Program Lobby",{"batch":self.batch}):
				p_lobby = frappe.get_doc("Program Lobby",{"batch":self.batch ,"date":self.date })
				p_lobby.append("lobby_child_details", {
					"child": self.facility,
					"program": self.program,
					"in_time": frappe.utils.get_datetime(),
				})
				p_lobby.save()
				self.append("check_in_records", {
					"child_id": self.child_id,
					"facility": self.facility,
					"instructors": self.instructors,
					"check_in_time": frappe.utils.get_datetime(),
					"duration" : 1800,
				})
				frappe.msgprint("Added to Lobby")
				self.child_id = ""
				self.parent_id = ""
				self.booking_id = ""
				self.active_tokens = ""
				self.course = ""
				self.child_name = ""
				self.parent_name = ""
				self.save()
				self.reload()
				return True
			else:
				p_lobby = frappe.new_doc("Program Lobby")
				p_lobby.company = self.company
				p_lobby.franchise = self.franchise
				p_lobby.venue = self.venue
				p_lobby.batch = self.batch
				p_lobby.append("lobby_child_details", {
					"child": self.facility,
					"program": self.program,
					"in_time": frappe.utils.get_datetime(),
				})
				p_lobby.save()
				self.append("check_in_records", {
					"child_id": self.child_id,
					"facility": self.facility,
					"instructors": self.instructors,
					"check_in_time": frappe.utils.get_datetime(),
					"duration" : 1800,
				})
				frappe.msgprint("Added to Lobby")
				self.child_id = ""
				self.parent_id = ""
				self.booking_id = ""
				self.active_tokens = ""
				self.course = ""
				self.child_name = ""
				self.parent_name = ""
				self.save()
				self.reload()
				return True
		else:
			frappe.msgprint("There is no Active Tokens")
		self.save()
		self.reload()
	# def before_submit(self):
	# 	self.invoice_submission()
	# 	self.customer_details_update()

	@frappe.whitelist()
	def check_tokens(self):
		if self.parent_id:
			parent_doc = frappe.get_doc("Parents",self.parent_id)
			print("Image is loding up",parent_doc.image)
			self.parent_image_file = parent_doc.image
		if self.child_id:
			child_doc = frappe.get_doc("Child Info",self.child_id)
			self.child_image_file = child_doc.image
			self.save()
			self.reload()
			if frappe.db.exists("Bookings", {"child_name":self.child_id}):
				booking_id =  frappe.get_doc("Bookings", {"child_name":self.child_id})
				if booking_id.total_active_tokens:
					self.booking_id = booking_id.name
					self.course = booking_id.course
					self.active_tokens = booking_id.total_active_tokens
					frappe.db.commit()
					return True
			else:
				# frappe.msgprint("title": "My message title","There is no Active Tokens",indicator="red")
				# frappe.msgprint("Please go to Bookings page for validations")
				frappe.msgprint(_("There is no Active Tokens Please go to Bookings page for validations"), title=_('Warning'), indicator='red')

