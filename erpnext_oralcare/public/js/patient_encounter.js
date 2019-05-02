frappe.ui.form.on("Patient Encounter", "patient", function(frm){
	console.log(frm)
})

frappe.ui.form.on("Patient Encounter", "onload", function(frm){
	alert('Test')
})
