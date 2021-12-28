// Copyright (c) 2021, tarunsairam2142 and contributors
// For license information, please see license.txt

frappe.ui.form.on('Instructors', {
	refresh: function(frm) {
		add_custom_buttons(frm);
	}
});
const add_custom_buttons = (frm) => {
	if (
		!frm.doc.start_time
	  ) {
		frm.add_custom_button(__("Start Timer"), function () {
			frm.call('start_timer').then((r) => {
				frm.reload_doc();
			  });
			  
		}).css("background-color","#ffa00a")
	}
	if (
		frm.doc.start_time
	  ) {
		frm.add_custom_button(__("End Timer"), function () {
			frm.call('end_timer').then((r) => {
				frm.reload_doc();
			  });
			  
		}).css("background-color","#ffa00a")
	}

};
