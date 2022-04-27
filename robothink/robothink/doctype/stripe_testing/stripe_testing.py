# Copyright (c) 2022, tarunsairam2142 and contributors
# For license information, please see license.txt
# import frappe
from frappe.model.document import Document
import frappe
import stripe
from frappe import _
from frappe.integrations.utils import create_request_log

class StripeTesting(Document):
    def validate(self):
        try : 

            if self.fetch_strip_payments:
                stripe_settings = frappe.get_doc("Stripe Settings", self.stripe_account)
                stripe.api_key = stripe_settings.get_password(fieldname="secret_key", raise_exception=False)
                # self.stripe_date =  str(stripe.PaymentIntent.list(limit=5))
                c_data = stripe.Customer.list(limit=100,starting_after="cus_IXB4EzVGwCvyjl")
                if c_data:
                    self.stripe_data =  str(c_data)
                    c = ""
                    for c_d in c_data["data"]:
                        phone = "None"
                        if c_d.phone:
                            phone = c_d.phone
                        subscriptions = "None"
                        if c_d.subscriptions:
                            subscriptions = c_d.subscriptions
                        c = c + "----------" + c_d.name + "," +  c_d.id + "," +  c_d.email  + "," +  phone + "," +  str(subscriptions)
                        self.append("child_customer_table", {
                            "customer_name": c_d.name,
                            "customer_id": c_d.id,
                            "mail_id": c_d.email,
                            "phone_number": phone,
                        })
                        c_doc = frappe.new_doc("Stripe Customer Data")
                        c_doc.customer_name = c_d.name
                        c_doc.customer_id = c_d.id
                        c_doc.mail_id = c_d.email
                        c_doc.phone_number = phone
                        c_doc.comments = str(subscriptions)
                        c_doc.insert()
                    self.customer_data = c
                else:
                    frappe.msgprint("no data coming")
                
        except Exception as e:
            frappe.msgprint(e)
