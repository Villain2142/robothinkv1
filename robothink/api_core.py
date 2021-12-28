from __future__ import unicode_literals
import frappe, base64, hashlib, hmac, json
from frappe import _
from datetime import datetime


@frappe.whitelist(allow_guest=True)
def api_data(*args):
    """
        Sales Order Cancelation and status change
    """
    test_data = json.loads(frappe.request.data)
    try:
        api_response = frappe.new_doc("Api Logs")
        api_response.title = "Data Inserted"
        api_response.api_data = str(test_data)
        api_response.api_reponse = "200"
        api_response.flags.ignore_permissions = True
        api_response.save()
        frappe.db.commit()
        return {"message":"Order Cancelled Successfully"}

    except Exception as e:
        api_response.title = "Data Called"
        api_response.api_data = str(test_data)
        api_response.api_reponse = str(e)
        api_response.flags.ignore_permissions = True
        api_response.save()
        frappe.db.commit()
        return {"message":e}

@frappe.whitelist(allow_guest=True)
def check_in(child_id):
    print("child_id,parent_id,booking_id,active_tokens,course,child_name,parent_name",child_id)
    return True
    # self.child_id = child_id
    # self.parent_id = parent_id
    # self.booking_id = booking_id
    # self.active_tokens = active_tokens
    # self.course = course
    # self.child_name = child_name
    # self.parent_name = parent_name
    # self.save()


@frappe.whitelist(allow_guest=True)
def check_out(child_id):
    print("child_id,parent_id,booking_id,active_tokens,course,child_name,parent_name",child_id)
    return True
    # self.child_id = child_id
    # self.parent_id = parent_id
    # self.booking_id = booking_id
    # self.active_tokens = active_tokens
    # self.course = course
    # self.child_name = child_name
    # self.parent_name = parent_name
    # self.save()