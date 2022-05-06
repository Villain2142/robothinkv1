# Copyright (c) 2022, tarunsairam2142 and contributors
# For license information, please see license.txt
# import frappe
from cmath import e
import frappe
from frappe.model.document import Document

class RobothinkFeePlan(Document):
	def after_insert(self):
		self.make_fee_category()

	def on_trash(self):
		self.delete_fee_category()

	def validate(self):
		self.validate_code()

	def validate_code(self):
		try:	
			if not frappe.db.exists("Fee Category",self.category_name):
				new_fee = frappe.new_doc("Fee Category")
				new_fee.category_name = self.category_name
				new_fee.flags.ignore_permissions = True
				new_fee.insert()
		except Exception as e:
			frappe.throw(e)
   
	def make_fee_category(self):
		try:	
			if not frappe.db.exists("Fee Category",self.category_name):
				new_fee = frappe.new_doc("Fee Category")
				new_fee.category_name = self.category_name
				new_fee.flags.ignore_permissions = True
				new_fee.insert()
		except Exception as e:
			frappe.throw(e)

	def delete_fee_category(self):
		try:	
			if frappe.db.exists("Fee Category",self.category_name):
				del_fee = frappe.get_doc("Fee Category",self.category_name)
				del_fee.flags.ignore_permissions = True
				del_fee.delete()
		except Exception as e:
			frappe.throw(e)
