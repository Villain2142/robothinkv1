# Copyright (c) 2022, tarunsairam2142 and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document

class FranchiseSales(Document):
    def validate(self):
        self.generate_report()
    def generate_report(self):
        conditions=''
        if self.franchise and self.company and self.start_date and self.end_date:
            if self.robothink_program and self.child:
                conditions += f"AND program = {self.robothink_program}"
            if self.child:
                conditions += f" AND child = {self.child}"
        if not self.start_date:
            start_date = add_months(today(), -1)
        if not self.end_date:
            end_date = add_days(today(), -1)

        payment_list = frappe.db.sql_list('''
            select name
            from `tabRoboThink Payment`
            where company=%s and franchise=%s and 
            transaction_date between %s and %s
            {0}
        '''.format(conditions), ( self.company,self.franchise ,self.start_date,self.end_date))
        if payment_list:
            for p in payment_list:
                self.program_transactions = None
                p_doc = frappe.get_doc("RoboThink Payment",p)
                self.append("program_transactions",{
                    "child" :  p_doc.child,
                    "booking_id" :  p_doc.booking_id,
                    "transaction_date" : p_doc.transaction_date,
                    "mode_of_payment" : p_doc.mode_of_payment,
                    "paid_amount" :  p_doc.paid_amount
                })