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

from erpnext.controllers.accounts_controller import get_taxes_and_charges
from frappe import throw, _
import frappe.defaults
from frappe.utils import getdate
from erpnext.controllers.buying_controller import BuyingController
from erpnext.accounts.utils import get_account_currency
from frappe.desk.notifications import clear_doctype_notifications
from frappe.model.mapper import get_mapped_doc
from erpnext.buying.utils import check_on_hold_or_closed_status
from erpnext.assets.doctype.asset.asset import get_asset_account, is_cwip_accounting_enabled
from erpnext.assets.doctype.asset_category.asset_category import get_asset_category_account
from frappe.utils.data import format_duration
from six import iteritems
from erpnext.stock.doctype.delivery_note.delivery_note import make_inter_company_transaction
from erpnext.accounts.doctype.payment_request.payment_request import make_payment_request, make_payment_entry

class ChildInfo(Document):
	def validate(self):
		self.validate_code()
	@frappe.whitelist()
	def validate_code(self):
		if self.parent_id:
			parent_doc = frappe.get_doc("Parents",self.parent_id)
			if parent_doc.child_details:
				child_list = []
				for x in parent_doc.child_details:
					child_list.append(x.child_link)
				if self.name not in child_list:
					parent_doc.append("child_details",{
						"child_link": self.name,
						"child_name": self.child_name,
						"gender":self.gender,
						"date_of_birth":self.date_of_birth,
						"any_health_conditions":self.any_health_conditions
					})
			else:
				parent_doc.append("child_details",{
					"child_link": self.name,
					"child_name": self.child_name,
					"gender":self.gender,
					"date_of_birth":self.date_of_birth,
					"any_health_conditions":self.any_health_conditions
				})
			parent_doc.save()
			parent_doc.reload()