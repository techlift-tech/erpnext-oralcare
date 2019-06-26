frappe.ui.form.off('Clinical Procedure', 'appointment')
frappe.ui.form.off('Clinical Procedure', 'practitioner')
frappe.ui.form.on('Clinical Procedure', {
	refresh: function(frm) {
	},
	encounter: function(frm) {
		if(frm.doc.encounter){
			frappe.call({
				"method": "frappe.client.get",
				args: {
					doctype: "Patient Encounter",
					name: frm.doc.encounter
				},
				callback: function (data) {
					frappe.model.set_value(frm.doctype,frm.docname, "patient", data.message.patient);
					frappe.model.set_value(frm.doctype,frm.docname, "appointment", data.message.appointment);
				}
			});
		}
		else{
			frappe.model.set_value(frm.doctype,frm.docname, "patient", '');
			frappe.model.set_value(frm.doctype,frm.docname, "appointment", '');
		}
	},
	on_submit: function(frm){
		if(frm.doc.encounter){
			frappe.set_route("Form", "Patient Encounter", frm.doc.encounter);
		}
	},
	practitioner: function(frm) {
	},
	appointment: function(frm) {
		if(frm.doc.appointment){
			frappe.call({
				"method": "frappe.client.get",
				args: {
					doctype: "Patient Appointment",
					name: frm.doc.appointment
				},
				callback: function (data) {
					frm.set_value("patient", data.message.patient);
					frm.set_value("procedure_template", data.message.procedure_template);
					frm.set_value("start_date", data.message.appointment_date);
					frm.set_value("start_time", data.message.appointment_time);
					frm.set_value("notes", data.message.notes);
					frm.set_value("service_unit", data.message.service_unit);
				}
			});
		}
	},
});


