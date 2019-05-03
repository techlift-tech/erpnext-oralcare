var draw_page = function(patient, me){
	console.log('test')
	frappe.model.with_doctype("Patient Medical Record", function() {
		me.page.list = new MedicalView({
			page_title: 'Medical Record',
			hide_refresh: true,
			page: me.page,
			page_name: frappe.get_route_str(),
			meta: frappe.get_meta('Patient Medical Record'),
			method: 'erpnext.healthcare.page.medical_record.medical_record.get_feed',
			args: {name: patient},
			parent: $("<div></div>").appendTo(me.page.main),
			show_filters: true,
			doctype: "Patient Medical Record",
			start: 0,
			page_length: 20,
			patient: patient
		});
		show_patient_info(patient, me);
		me.page.list.show();
	});
}

MedicalView = class MedicalView extends frappe.views.BaseList{
	constructor(opts){
		super(opts)
	}

	render(){
		console.log('rrr')
		var me = this;
		var wrapper = me.page.main.find(".result-list").get(0);
		this.data.map(function (value) {
			var row = $('<div class="list-row">').data("data", value).appendTo(me.$result).get(0);
			new frappe.medical_record.Feed(row, value);
		});
	}

	setup_page(){
	}

	setup_side_bar(){
	}

	get_args() {
		return {
			start: this.start,
			page_length: this.page_length,
			name: this.patient
		};
	}

	setup_defaults() {
		this.fields = []	
		this.filters = []
	}
}
