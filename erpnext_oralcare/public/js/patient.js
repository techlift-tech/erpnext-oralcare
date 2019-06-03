frappe.ui.form.on("Patient", {
	setup: function(frm) {
		frm.dashboard.init_data()
		var dashboard_object = {
			items: ['Conservative Dentistry and Endondontics', 'Oral Medicine and Diagnosis', 'Oral Suegery and Trauma', 'Periodontology', 'Prosthodontics'],
			label: 'Case History'
		}
		frm.dashboard.add_transactions(dashboard_object)
	},
	refresh: function(frm) {
	}
});


