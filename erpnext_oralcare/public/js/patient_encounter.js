frappe.ui.form.on("Patient Encounter", "patient", function(frm){
	console.log(frm)
	if(frm.doc.patient){
		frappe.call({
			"method": "erpnext.healthcare.doctype.patient.patient.get_patient_detail",
			args: {
				patient: frm.doc.patient
			},
			callback: function (data) {
				console.log(data.message)
			}
		});
	}
})

frappe.ui.form.on("Patient Encounter", "onload", function(frm){
	alert('Test')
})
