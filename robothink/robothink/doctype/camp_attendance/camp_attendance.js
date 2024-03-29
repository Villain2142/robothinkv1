// Copyright (c) 2021, tarunsairam2142 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Camp Attendance', {
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
	franchise: function (frm) {
		if (frm.doc.franchise) {
			frm.set_df_property('franchise', 'hidden', 1);
		}
	},
	venue: function (frm) {
		if (frm.doc.venue) {
			frm.set_df_property('venue', 'hidden', 1);
		}
	},
	parent_id: function (frm) {
		frm.add_custom_button(__("Clear"), function () {
			frm.set_df_property('parent_id', 'hidden', 0);
			frm.set_value("parent_name", "");
			frm.set_value("child_name", "");
			// Tu codigo ...
		}).css("background-color","#ffa00a")
		frm.set_value("child_name", "");
		frm.set_value("child_id", "");
		frm.set_df_property('parent_id', 'hidden', 1);
		frm.set_df_property('child_id', 'hidden', 0);
	},
	child_id: function (frm) {
		if (frm.doc.child_id) {
			frm.add_custom_button(__("Start Timer"), function () {
				add_child_record(frm);
				frm.reload_doc();
				// frm.call('start_timer').then((r) => {
				// 	});
				// Tu codigo ...
			}).css("background-color","#98d85b")
		}
	},
});



const set_query = (frm) => {
	frm.set_query('child_id', () => {
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


const add_custom_buttons = (frm) => {
	frm.add_custom_button(__("Clear"), function () {
		frm.set_df_property('parent_id', 'hidden', 0);
		frm.set_value("parent_name", "");
		frm.set_value("child_name", "");
		// Tu codigo ...
	}).css("background-color","#ffa00a")
	if (frm.doc.child_id) {
		frm.add_custom_button(__("Start Timer"), function () {
			add_child_record(frm);
			// frm.call('start_timer').then((r) => {
			// 	});
			// Tu codigo ...
		}).css("background-color","#98d85b")
	}
};

const add_child_record = (frm) => {
	frappe.call({
		doc: frm.doc,
		method: 'child_records_update',
		callback: function(data) {
			if (data.message) {
				frm.reload_doc();
			}
		}
	});
  }
