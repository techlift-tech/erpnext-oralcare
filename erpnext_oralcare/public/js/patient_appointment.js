console.log('sss')
frappe.ui.form.on("Patient Appointment", {
	after_save: function(frm) {
		frappe.set_route("List", "Patient Appointment", "Calendar", "Default");
	}
});
