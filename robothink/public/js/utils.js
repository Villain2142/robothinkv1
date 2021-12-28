// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt
// frappe.provide("robothink");
// frappe.provide("robothink.utils");


// frappe.form.link_formatters['Parents'] = function(value, doc) {
// 	if (doc && value && doc.item_name && doc.parent_name !== value) {
// 		return value + ': ' + doc.parent_name;
// 	} else if (!value && doc.doctype && doc.parent_name) {
// 		// format blank value in child table
// 		return doc.parent_name;
// 	} else {
// 		// if value is blank in report view or item code and name are the same, return as is
// 		return value;
// 	}
// }