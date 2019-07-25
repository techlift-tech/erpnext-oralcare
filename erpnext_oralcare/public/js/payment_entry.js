
frappe.ui.form.on('Payment Entry', {
	refresh: function(frm) {
		var series = ''
		if(frm.doc.payment_type == 'Receive') {
			series = 'REC.YY.MM.####'
		} else if(frm.doc.payment_type == 'Pay') {
			series = 'PAY.YY.MM.####'
		} else {
			series = 'INT.YY.MM.####'
		}
		frm.set_value('naming_series', series)
	},
	payment_type: function(frm) {
		var series = ''
		if(frm.doc.payment_type == 'Receive') {
			series = 'REC.YY.MM.####'
		} else if(frm.doc.payment_type == 'Pay') {
			series = 'PAY.YY.MM.####'
		} else {
			series = 'INT.YY.MM.####'
		}
		frm.set_value('naming_series', series)
	}
})
