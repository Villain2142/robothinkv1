# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt

from __future__ import unicode_literals

import frappe
from frappe.exceptions import DocstatusTransitionError
from frappe.utils import now
from frappe import _

@frappe.whitelist(allow_guest=True)
def get_context():
    docname  = "FR:0000001"
    context = []
    doc = frappe.get_doc("Franchise", docname)
    structured_learning_d = frappe.get_list('Manage Courses', filters={'structured_learning': 1}, fields=['name1','attach_image','full_week_price','venue_name','small_note'])
    workshops_d = frappe.get_list('Manage Courses', filters={'workshops': 1}, fields=['name1','attach_image','full_week_price','venue_name','small_note'])
    holiday_camps_d = frappe.get_list('Manage Courses', filters={'holiday_camps': 1}, fields=['name1','attach_image','full_week_price','venue_name','small_note'])
    after_school_clubs_d = frappe.get_list('Manage Courses', filters={'after_school_clubs': 1}, fields=['name1','attach_image','full_week_price','venue_name','small_note'])
    birthday_party_d = frappe.get_list('Manage Courses', filters={'birthday_party': 1}, fields=['name1','attach_image','full_week_price','venue_name','small_note'])

    context.append(structured_learning_d)
    context.append(workshops_d)
    context.append(holiday_camps_d)
    context.append(after_school_clubs_d)
    context.append(birthday_party_d)

    data =  {
        "doc": doc,
        "context": context
        }



    # structured_learning_d = frappe.db.get_list('Manage Courses',{"structured_learning": 1}, fields)


    return data
