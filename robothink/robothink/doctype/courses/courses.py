# Copyright (c) 2021, tarunsairam2142 and contributors
# For license information, please see license.txt

# import frappe
from cmath import e
import frappe
from frappe.model.document import Document

class Courses(Document):
	def after_insert(self):
		self.make_course()
	def validate(self):
		self.validate_code()

	def on_trash(self):
		self.delete_course()


	def make_course(self):
		try:	
			if not frappe.db.exists("Course",self.name):
				new_course = frappe.new_doc("Course")
				new_course.course_name = self.course_name
				new_course.flags.ignore_permissions = True
				new_course.insert()
		except Exception as e:
			frappe.throw(e)

	def validate_code(self):

		try:	
			if not frappe.db.exists("Course",self.name):
				new_course = frappe.new_doc("Course")
				new_course.course_name = self.course_name
				new_course.flags.ignore_permissions = True
				new_course.insert()
		except Exception as e:
			frappe.throw(e)
   
		for x in self.content:
			lesson_doc =  frappe.get_doc("Lessons",x.lesson)
			if lesson_doc.courses != self.course_name:
				lesson_doc.courses = self.course_name
				lesson_doc.save()


	def delete_course(self):
		try:	
			if frappe.db.exists("Course",self.name):
				del_course = frappe.get_doc("Course",self.name)
				del_course.flags.ignore_permissions = True
				del_course.delete()
		except Exception as e:
			frappe.throw(e)

