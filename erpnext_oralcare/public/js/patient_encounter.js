frappe.ui.form.on("Patient Encounter", "patient", function(frm){
	console.log(frm)
	if(frm.doc.patient){
		frappe.call({
			"method": "erpnext.healthcare.doctype.patient.patient.get_patient_detail",
			args: {
				patient: frm.doc.patient
			},
			callback: function (data) {
				var blood_group = data.message.blood_group
				var allergies = data.message.allergies
				var medication = data.message.medication
				var alchohol_current_use = data.message.alchohol_current_use
				var alchohol_past_use = data.message.alchohol_past_use
				var tobaco_current_use = data.message.tobaco_current_use
				var tobaco_past_use = data.message.tobaco_past_use
				var medical_history = data.message.medical_history
				var surgical_history = data.message.surgical_history

				frappe.mode.set_value(frm.doctype, frm.docname, "important_points", "<p>Palash</p>")

				console.log(data.message)
			}
		});
	}
})

frappe.ui.form.on("Patient Encounter", "onload", function(frm){
	alert('Test')
})
