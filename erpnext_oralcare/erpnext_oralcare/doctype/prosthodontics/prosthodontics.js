// Copyright (c) 2019, Techlift and contributors
// For license information, please see license.txt

frappe.ui.form.on('Prosthodontics', {
	// refresh: function(frm) {

	// }
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
