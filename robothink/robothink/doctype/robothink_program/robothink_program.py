# Copyright (c) 2022, tarunsairam2142 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class RobothinkProgram(Document):
	def after_insert(self):
		self.make_program()
		self.make_batches()
		self.make_plans()

  
	def validate(self):
		if not self.is_new():
			self.validate_program()
			# self.validate_plans()
			self.validate_batches()

	def on_trash(self):
		self.delete_program()
		self.delete_batches()


	def make_program(self):
		try:	
			if not frappe.db.exists("Program",self.name):
				new_program = frappe.new_doc("Program")
				new_program.program_name = self.name
				for c in self.courses:
					new_program.append("courses",{
						"course": c.courses
					})
				new_program.flags.ignore_permissions = True
				new_program.insert()
			if self.courses:
				for c in self.courses:
					self.main_course = c.courses
		except Exception as e:
			frappe.throw(e)

	def validate_program(self):
		try:	
			if not frappe.db.exists("Program",self.name):
				new_program = frappe.new_doc("Program")
				new_program.program_name = self.name
				for c in self.courses:
						new_program.append("courses",{
						"course": c.courses
					})
				new_program.flags.ignore_permissions = True
				new_program.insert()
			else:
				del_program = frappe.get_doc("Program",self.name)
				del_program.flags.ignore_permissions = True
				del_program.delete()
				new_program = frappe.new_doc("Program")
				new_program.program_name = self.name
				for c in self.courses:
						new_program.append("courses",{
						"course": c.courses
					})
				new_program.flags.ignore_permissions = True
				new_program.insert()
			if self.courses:
				for c in self.courses:
					self.main_course = c.courses
		except Exception as e:
			frappe.throw(e)

	def delete_program(self):
		try:	
			if frappe.db.exists("Program",self.name):
				del_program = frappe.get_doc("Program",self.name)
				del_program.flags.ignore_permissions = True
				del_program.delete()
		except Exception as e:
			frappe.throw(e)



	def make_batches(self):
		try:
			if self.program_schedule:
				for b in self.program_schedule:
					if not b.batches:
						new_batch = frappe.new_doc("Batches")
						new_batch.day = b.day
						new_batch.from_time = b.start_time
						new_batch.to_time = b.end_time
						new_batch.no_of_seats = b.no_of_seats
						new_batch.venue = self.venue
						new_batch.program = self.name
						new_batch.available_seats = b.no_of_seats
						new_batch.ignore_permissions = True
						new_batch.insert()
						b.batches = new_batch.name
						b.available_seats = new_batch.no_of_seats
						frappe.db.commit()
		except Exception as e:
			frappe.throw(e)
	def validate_batches(self):
		try:
			if self.program_schedule:
				for b in self.program_schedule:
					if not b.batches:
						new_batch = frappe.new_doc("Batches")
						new_batch.day = b.day
						new_batch.from_time = b.start_time
						new_batch.to_time = b.end_time
						new_batch.no_of_seats = b.no_of_seats
						new_batch.venue = self.venue
						new_batch.program = self.name
						new_batch.available_seats = b.no_of_seats
						new_batch.ignore_permissions = True
						new_batch.insert()
						b.batches = new_batch.name
						b.available_seats = new_batch.no_of_seats
						frappe.db.commit()
					else:
						batch = frappe.get_doc("Batches",b.batches)
						b.available_seats = batch.available_seats
						b.occupied_seats = batch.occupied_seats
		except Exception as e:
			frappe.throw(e)


	def delete_batches(self):
		try:
			if self.program_schedule:
				for b in self.program_schedule:
					if frappe.db.exists("Batches",b.batches):
						del_batch = frappe.get_doc("Batches",b.batches)
						del_batch.flags.ignore_permissions = True
						del_batch.delete()
		except Exception as e:
			frappe.throw(e)



	def make_plans(self):
		try:
			if self.plans:
				for p in self.plans:
					if p.fees_category:
						plan = frappe.get_doc("Robothink Fee Plan",p.fees_category)
						plan.amount = p.amount
						plan.program = self.name
						plan.ignore_permissions = True
						plan.save()
		except Exception as e:
			frappe.throw(e)