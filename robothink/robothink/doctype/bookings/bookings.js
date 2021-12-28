// Copyright (c) 2021, tarunsairam2142 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bookings', {
	onload: function(frm) {
		if (frm.is_new()) {
			frm.trigger('set_company');
		}
	},
	set_company: function(frm) {
		frappe.call({
			doc: frm.doc,
			method: 'select_company',
			callback: function(data) {
				if (data.message) {
					frm.set_value("company", data.message);
				}
			}
		});
	},
	refresh: function(frm) {
		set_query(frm);	
	},
});
const set_query = (frm) => {
	frm.set_query('child_name', () => {
		if (frm.doc.parent_id) {
			return {
				filters: {
					parent_id: frm.doc.parent_id
				}
			}
		}
	});
	// frm.call('get_payment_status');
	// frm.set_query('address_name', () => {
	//   if (frm.doc.customer) {
	// 	return {
	// 	  query: 'frappe.contacts.doctype.address.address.address_query',
	// 	  filters: {
	// 		link_doctype: "Customer",
	// 		link_name: frm.doc.customer
	// 	  }
	// 	};
	//   }
	// });
	frm.set_query('venue', () => {
		if (frm.doc.franchise) {
			return {
				filters: {
					franschise: frm.doc.franchise
				}
			}
		}
	});
};