# Copyright (c) 2022, tarunsairam2142 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ProgramLobby(Document):
	pass


	@frappe.whitelist()
	def child_records_update(self):
		if len(self.lobby_child_details) > 0:
			if frappe.db.exists("Class Records",{"child_name":self.child_id}):
				if frappe.db.exists("Class Records",{"child_name":self.child_id,"status":"Out"}):
					class_record = frappe.get_doc("Class Records",{"child_name":self.child_id})
					class_record.status = "In"
					class_record.start_time = frappe.utils.get_datetime()
					class_record.append("date_wise", {
						"room": self.facility,
						"instructor": self.instructors,
						"check_in": frappe.utils.get_datetime(),
					})
					class_record.save()
				else:
					frappe.msgprint("Class Record already Exists")
					self.child_id = ""
			else:
				class_record = frappe.new_doc("Class Records")
				class_record.child_name = self.child_id
				class_record.venue = self.venue
				class_record.status = "In"
				class_record.start_time = frappe.utils.get_datetime()
				class_record.append("date_wise", {
					"room": self.facility,
					"instructor": self.instructors,
					"check_in": frappe.utils.get_datetime(),
				})
				class_record.save()
		else:
			frappe.msgprint("There is no Active Tokens")
		self.save()
		self.reload()
	# def before_submit(self):
	# 	self.invoice_submission()
	# 	self.customer_details_update()