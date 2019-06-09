// Copyright (c) 2019, Techlift and contributors
// For license information, please see license.txt

frappe.ui.form.on('Conservative Dentistry and Endondontics', {
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
					frappe.model.set_value(frm.doctype,frm.docname, "patient_appointment", data.message.appointment);
				}
			});
		}
		else{
			frappe.model.set_value(frm.doctype,frm.docname, "patient", '');
			frappe.model.set_value(frm.doctype,frm.docname, "patient_appointment", '');
		}
	}	
});

/*frappe.ui.form.on("Patient Encounter", "appointment", function(frm){
	if(frm.doc.appointment){
		frappe.call({
			"method": "frappe.client.get",
			args: {
				doctype: "Patient Appointment",
				name: frm.doc.appointment
			},
			callback: function (data) {
				frappe.model.set_value(frm.doctype,frm.docname, "patient", data.message.patient);
				frappe.model.set_value(frm.doctype,frm.docname, "type", data.message.appointment_type);
				frappe.model.set_value(frm.doctype,frm.docname, "practitioner", data.message.practitioner);
				frappe.model.set_value(frm.doctype,frm.docname, "invoiced", data.message.invoiced);
			}
		});
	}
	else{
		frappe.model.set_value(frm.doctype,frm.docname, "patient", "");
		frappe.model.set_value(frm.doctype,frm.docname, "type", "");
		frappe.model.set_value(frm.doctype,frm.docname, "practitioner", "");
		frappe.model.set_value(frm.doctype,frm.docname, "invoiced", 0);
	}
});*/


