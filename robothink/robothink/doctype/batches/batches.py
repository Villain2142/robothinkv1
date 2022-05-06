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


class Batches(Document):

	def validate(self):
		self.validate_code()

	@frappe.whitelist()
	def validate_code(self):
		try:
			if self.program:
				program = frappe.get_doc("Robothink Program",self.program)
				if program.program_schedule:
					for b in program.program_schedule:
						if b.batches == self.name:
							frappe.db.set_value("Program Schedule",b.name,"occupied_seats",self.occupied_seats)
							frappe.db.set_value("Program Schedule",b.name,"available_seats",self.available_seats)
		except Exception as e:
			print (e)