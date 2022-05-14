from __future__ import unicode_literals
from cgi import test
import frappe, base64, hashlib, hmac, json
from frappe import _
from datetime import datetime
import requests


@frappe.whitelist(allow_guest=True)
def insert_parent_ghl(doc,method=None):
    """
        Sales Order Cancelation and status change
    """        
    url = "https://rest.gohighlevel.com/v1/contacts/"
    headers = {
        "Authorization": "Bearer bdcd833f-f0a1-415e-8281-1b08da72bcee",
        "Content-Type": "application/json" 
    }
    if doc.lead_connector_id and doc.lead_connector_sync:
        try:
            child_details = ""
            for child in doc.child_details:
                child_details += str(child.child_name) + ","
            url = url + doc.lead_connector_id
            phone  =str(doc.phone)
            if phone.startswith('44'):
                phone  = "+" + phone
            elif phone.startswith('0'):
                phone  = "+44" + phone[1:]
            else:
                phone  = "+44" + phone
            payload = json.dumps({
                "email":str(doc.email),
                "phone": phone,
                "name":str(doc.parent_name),
                "address1":str(doc.address_line_1),
                "city": str(doc.county),
                "state":"AL",
                "country":"UK",
                "postalCode":str(doc.pincode),
                "customField":{
                    "registered_date": str(doc.registered_date),
                    "p_status": str(doc.status),
                    "pending_amt": str(doc.pending_amt),
                    "child_details": child_details
                }
            })
            response = requests.request("PUT", url, headers=headers, data=payload)
            api_response = frappe.new_doc("Api Logs")
            api_response.title = "Data Inserted"
            api_response.api_data = str(response.text) + str(payload)
            api_response.api_reponse = "200"
            api_response.flags.ignore_permissions = True
            api_response.save()
            frappe.db.commit()

        except Exception as e:
            api_response = frappe.new_doc("Api Logs")
            api_response.title = "Data Called"
            api_response.api_data = str(doc)
            api_response.api_reponse = str(e)
            api_response.flags.ignore_permissions = True
            api_response.save()
            frappe.db.commit()
    else:
        try:
            child_details = ""
            for child in doc.child_details:
                child_details += str(child.child_name) + ","
            phone  =str(doc.phone)
            if phone.startswith('44'):
                phone  = "+" + phone
            elif phone.startswith('0'):
                phone  = "+44" + phone[1:]
            else:
                phone  = "+44" + phone
            payload = json.dumps({
                "email":str(doc.email),
                "phone": phone,
                "name":str(doc.parent_name),
                "address1":str(doc.address_line_1),
                "city": str(doc.county),
                "state":"AL",
                "country":"UK",
                "postalCode":str(doc.pincode),
                "customField":{
                    "registered_date": str(doc.registered_date),
                    "p_status": str(doc.status),
                    "pending_amt": str(doc.pending_amt),
                    "child_details": child_details
                }
            })
            response = requests.request("POST", url, headers=headers, data=payload)
            r_data = response.json()
            r_data = r_data["contact"]
            doc.lead_connector_id = r_data["id"]
            doc.lead_connector_sync = 1
            api_response = frappe.new_doc("Api Logs")
            api_response.title = "Data Inserted"
            api_response.api_data = str(r_data["id"]) + str(payload)
            api_response.api_reponse = "200"
            api_response.flags.ignore_permissions = True
            api_response.save()
            frappe.db.commit()

        except Exception as e:
            api_response = frappe.new_doc("Api Logs")
            api_response.title = "Data Called"
            api_response.api_data = str(doc)
            api_response.api_reponse = str(e)
            api_response.flags.ignore_permissions = True
            api_response.save()
            frappe.db.commit()

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
        api_response = frappe.new_doc("Api Logs")
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


@frappe.whitelist(allow_guest=True)
def make_payment(**args):
    # data = frappe._dict(json.loads(data))
    print(args)
    data = json.loads(args["data"])
    doc=  frappe.get_doc("Bookings",args["doc"])
    new_payment =  frappe.new_doc("RoboThink Payment")
    new_payment.child = doc.child_name
    new_payment.parents = doc.parent_id
    new_payment.transaction_date = data["date"]
    new_payment.company = doc.company
    new_payment.program = doc.select_program
    new_payment.booking_id = doc.name
    new_payment.plan = doc.plan
    new_payment.due_amount = doc.due_amount
    new_payment.mode_of_payment = data["mode_of_payment"]
    new_payment.paid_amount = data["paid_amount"]
    new_payment.flags.ignore_permissions = True
    new_payment.save()
    new_payment.submit()
    p_amt = float(doc.paid_amount)+float(data["paid_amount"])
    due= float(doc.amount)-p_amt
    frappe.db.set_value("Bookings",doc.name,"due_amount",due)
    frappe.db.set_value("Bookings",doc.name,"paid_amount",p_amt)
    frappe.db.set_value("Bookings",doc.name,"last_payment_date",data["date"])
    if due != 0:
        frappe.db.set_value("Bookings",doc.name,"process_status","Payment Pending")
    else:
        frappe.db.set_value("Bookings",doc.name,"process_status","Completed")
    if doc.parent_id:
        p_doc = frappe.get_doc("Parents",doc.parent_id)
        p_doc.append("booking_transaction",{
            "booking_id": doc.name,
            "transaction_date" : data["date"],
            "mode_of_payment" :data["mode_of_payment"],
            "paid_amount" : data["paid_amount"]
        })
        p_doc.flags.ignore_permissions = True
        p_doc.save()
        p_doc.reload()
    if doc.select_program:
        rp_doc = frappe.get_doc("Robothink Program",doc.select_program)
        if rp_doc.total_amount_received:
            rp_doc.total_amount_received += data["paid_amount"]
        rp_doc.append("program_transactions",{
            "child": doc.child_name,
            "booking_id": doc.name,
            "transaction_date" : data["date"],
            "mode_of_payment" :data["mode_of_payment"],
            "paid_amount" : data["paid_amount"]
        })
        rp_doc.flags.ignore_permissions = True
        rp_doc.save()
        rp_doc.reload()
    return True




@frappe.whitelist(allow_guest=True)
def api_class_records_data(*args):
    """
        API call for Class record details
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
        data = {}
        child_name  = test_data["child_name"]
        class_record = frappe.get_doc('Class Records',{"child_name": child_name}, ignore_permissions=True)
        data["class_record"] = class_record

        return data

    except Exception as e:
        api_response = frappe.new_doc("Api Logs")
        api_response.title = "Data Called"
        api_response.api_data = str(test_data)
        api_response.api_reponse = str(e)
        api_response.flags.ignore_permissions = True
        api_response.save()
        frappe.db.commit()
        return e

@frappe.whitelist(allow_guest=True)
def api_parent_data(*args):
    """
        API call for parent details
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
        data = {}
        doc_name  = test_data["p_doc"]
        parent_doc = frappe.get_doc("Parents",doc_name, ignore_permissions=True)
        data["parent"] = parent_doc
        childs = frappe.get_list('Child Info', filters={'parent_id': parent_doc.name}, fields=['child_name','gender','date_of_birth','schools','any_health_conditions','booking_id','name'], ignore_permissions=True)
        no = 0
        for x in childs:
            no += 1
            x["no"] = no
            if x.booking_id:
                booking_doc = frappe.get_doc("Bookings",x.booking_id)
                x["status"] = booking_doc.status
                x["used_tokens"] = booking_doc.used_tokens
                x["available_tokens"] = booking_doc.available_tokens
                x["total_active_tokens"] = booking_doc.total_active_tokens
                x["franchise"] = booking_doc.franchise
                x["venue_name"] = booking_doc.venue_name
                x["batch_id"] = booking_doc.batch_id
                x["process_status"] = booking_doc.process_status
                x["course"] = booking_doc.course
                x["last_payment_date"] = booking_doc.last_payment_date
                x["booking_amount"] = booking_doc.booking_amount
        data["childs"] = childs
        return data

    except Exception as e:
        api_response = frappe.new_doc("Api Logs")
        api_response.title = "Data Called"
        api_response.api_data = str(test_data)
        api_response.api_reponse = str(e)
        api_response.flags.ignore_permissions = True
        api_response.save()
        frappe.db.commit()
        return e