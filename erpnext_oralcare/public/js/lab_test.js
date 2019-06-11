frappe.ui.form.on('Lab Test', {
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
				}
			});
		}
		else{
			frappe.model.set_value(frm.doctype,frm.docname, "patient", '');
		}
	},
	on_submit: function(frm){
		if(frm.doc.encounter){
			frappe.set_route("Form", "Patient Encounter", frm.doc.encounter);
		}
	}
});


