frappe.ui.form.on("Patient Encounter", "patient", function(frm){
	console.log(frm)
	if(frm.doc.patient){
		frappe.call({
			"method": "erpnext.healthcare.doctype.patient.patient.get_patient_detail",
			args: {
				patient: frm.doc.patient
			},
			callback: function (data) {
				var blood_group = data.message.blood_group || ''
				var allergies = data.message.allergies || ''
				var medication = data.message.medication || ''
				var alchohol_current_use = data.message.alcohol_current_use || ''
				var alchohol_past_use = data.message.alcohol_past_use || ''
				var tobaco_current_use = data.message.tobacco_current_use || ''
				var tobaco_past_use = data.message.tobacco_past_use || ''
				var medical_history = data.message.medical_history || ''
				var surgical_history = data.message.surgical_history || ''

				//frappe.model.set_value(frm.doctype, frm.docname, "important_points", "<b>Palash</b>")

				var html_to_show = `
					<b>Blood Group: </b>${blood_group}<br>
					<b>Allergies: </b>${allergies}<br>
					<b>Medication: </b>${medication}<br>
					<b>Alchohol Current Use: </b>${alchohol_current_use} <b>Alcohol Past User: </b>${alchohol_past_use}<br>
					<b>Tobaco Current Use: </b>${tobaco_current_use} <b>Tobaco Past User: </b>${tobaco_past_use}<br>
					<b>Medical History: </b>${medical_history}<br>
					<b>Surgical History: </b>${surgical_history}<br>
				`

				frm.fields_dict.important_points.html(html_to_show)

				console.log(data.message)
			}
		});
	}
})

frappe.ui.form.on("Patient Encounter", "onload", function(frm){
	frm.fields_dict.important_points.html('')
if(frm.doc.patient){
		frappe.call({
			"method": "erpnext.healthcare.doctype.patient.patient.get_patient_detail",
			args: {
				patient: frm.doc.patient
			},
			callback: function (data) {
				var blood_group = data.message.blood_group || ''
				var allergies = data.message.allergies || ''
				var medication = data.message.medication || ''
				var alchohol_current_use = data.message.alcohol_current_use || ''
				var alchohol_past_use = data.message.alcohol_past_use || ''
				var tobaco_current_use = data.message.tobacco_current_use || ''
				var tobaco_past_use = data.message.tobacco_past_use || ''
				var medical_history = data.message.medical_history || ''
				var surgical_history = data.message.surgical_history || ''

				//frappe.model.set_value(frm.doctype, frm.docname, "important_points", "<b>Palash</b>")

				var html_to_show = `
					<b>Blood Group: </b>${blood_group}<br>
					<b>Allergies: </b>${allergies}<br>
					<b>Medication: </b>${medication}<br>
					<b>Alchohol Current Use: </b>${alchohol_current_use} <b>Alcohol Past User: </b>${alchohol_past_use}<br>
					<b>Tobaco Current Use: </b>${tobaco_current_use} <b>Tobaco Past User: </b>${tobaco_past_use}<br>
					<b>Medical History: </b>${medical_history}<br>
					<b>Surgical History: </b>${surgical_history}<br>
				`

				frm.fields_dict.important_points.html(html_to_show)

				console.log(data.message)
			}
		});
	}

})
