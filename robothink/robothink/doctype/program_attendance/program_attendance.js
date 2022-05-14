// Copyright (c) 2022, tarunsairam2142 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Program Attendance', {
	refresh: function(frm) {
		set_query(frm);
		add_custom_buttons(frm);
		
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

	frm.set_query('venue', () => {
		if (frm.doc.franchise) {
			return {
				filters: {
					franschise: frm.doc.franchise
				}
			}
		}
	});
	frm.set_query('batch', () => {
		if (frm.doc.day) {
			return {
				filters: {
					day: frm.doc.day,
					company:frm.doc.company
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
		frm.set_df_property('child_id', 'hidden', 1);
		frappe.call({
			doc: frm.doc,
			method: 'check_tokens',
			callback: function(data) {
				if (data.message) {
					frm.add_custom_button(__("Start Timer"), function () {
						add_child_record(frm);
						// frm.call('start_timer').then((r) => {
						// 	});
						// Tu codigo ...
					}).css("background-color","#98d85b")
				}
			}
		});
	}

};