# Copyright (c) 2021, tarunsairam2142 and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document

class Courses(Document):
	def validate(self):
		self.validate_code()
	def validate_code(self):
		for x in self.content:
			lesson_doc =  frappe.get_doc("Lessons",x.lesson)
			if lesson_doc.courses != self.course_name:
				lesson_doc.courses = self.course_name
				lesson_doc.save()

