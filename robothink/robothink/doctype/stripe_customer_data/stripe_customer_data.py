# Copyright (c) 2022, tarunsairam2142 and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
import frappe
import stripe
from frappe import _
from frappe.integrations.utils import create_request_log

class StripeCustomerData(Document):
    def validate(self):

        if frappe.db.exists("Parents",{"email": self.mail_id}):
            p_doc = frappe.get_doc("Parents",{"email": self.mail_id})
            self.parent_doc = p_doc.name
            frappe.db.commit()

    # def validate(self):
    #     if self.fetch_strip_payments:
    #         stripe_settings = frappe.get_doc("Stripe Settings", self.stripe_account)
    #         stripe.api_key = stripe_settings.get_password(fieldname="secret_key", raise_exception=False)
    #         # self.stripe_date =  str(stripe.PaymentIntent.list(limit=5))
    #         c_data = stripe.Customer.list(limit=800)
    #         self.stripe_data =  str(c_data)
    #         c = ""
    #         for c_d in c_data["data"]:
    #             c = c + "," + c_d["name"]
    #             self.append("stripe_customer_records", {
    #                 "customer_name": c_d["name"],
    #                 "customer_id": c_d["id"],
    #                 "mail_id": c_d["email"],
    #                 "phone_number": c_d["phone"],
    #                 "comments": c_d["subscriptions"],
    #             })
    #         self.customer_data = c
    #     if self.stripe_customer_records:
    #         for c in self.stripe_customer_records:
    #             if frappe.db.exists("Parents",{"email": c.mail_id}):
    #                 p_doc = frappe.get_doc("Parents",{"email": c.mail_id})
    #                 c.parent_doc = p_doc.name
