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
		add_custom_buttons(frm);
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
	frm.set_query('course', () => {
		if (frm.doc.select_program) {
			return {
				filters: {
					parent: frm.doc.select_program
				}
			}
		}
	});
	frm.set_query('plan', () => {
		if (frm.doc.select_program) {
			return {
				filters: {
					program: frm.doc.select_program
				}
			}
		}
	});
	frm.set_query('batches', () => {
		if (frm.doc.select_program) {
			return {
				filters: {
					program: frm.doc.select_program
				}
			}
		}
	});
};

const add_custom_buttons = (frm) => {
	if (frm.doc.docstatus === 1) {
		frm.add_custom_button(__('Make Payment'), function () {
			let d = new frappe.ui.Dialog({
				title: 'Enter details',
				fields: [
					{
						label: 'Mode of Payment',
						fieldname: 'mode_of_payment',
						fieldtype: 'Select',
						options: ["Cash", "Stripe", "Child Care Voucher", "Other"],
						reqd: 1
					},
					{
						label: 'Date',
						fieldname: 'date',
						fieldtype: 'Date',
						reqd: 1
					},
					{
						label: 'Paid Amount',
						fieldname: 'paid_amount',
						fieldtype: 'Currency',
						reqd: 1
					}
				],
				primary_action_label: 'Submit',
				primary_action: function() {
					var data = d.get_values();
					frappe.call({
						method: "robothink.api_core.make_payment",
						args: {
							data: data,
							doc: frm.doc.name,
						},
						callback: function(data) {
							if (data.message) {
								frm.reload_doc();
							}
						}
					});
					d.hide();
				},
			});
			
			d.show();
		}, __('Actions'));
	}

};

