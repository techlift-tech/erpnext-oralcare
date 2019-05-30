var show_patient_info = function(patient, me){
	frappe.call({
		"method": "erpnext.healthcare.doctype.patient.patient.get_patient_detail",
		args: {
			patient: patient
		},
		callback: function (r) {
			var data = r.message;
			var details = "";
			if(data.image) details += "<img src='" + data.image + "'>";
			if(data.email) details += "<br><b>Email :</b> " + data.email;
			if(data.mobile) details += "<br><b>Mobile :</b> " + data.mobile;
			if(data.occupation) details += "<br><b>Occupation :</b> " + data.occupation;
			if(data.blood_group) details += "<br><b>Blood group : </b> " + data.blood_group;
			if(data.allergies) details +=  "<br><br><b>Allergies : </b> "+  data.allergies;
			if(data.medication) details +=  "<br><b>Medication : </b> "+  data.medication;
			if(data.alcohol_current_use) details +=  "<br><br><b>Alcohol use : </b> "+  data.alcohol_current_use;
			if(data.alcohol_past_use) details +=  "<br><b>Alcohol past use : </b> "+  data.alcohol_past_use;
			if(data.tobacco_current_use) details +=  "<br><b>Tobacco use : </b> "+  data.tobacco_current_use;
			if(data.tobacco_past_use) details +=  "<br><b>Tobacco past use : </b> "+  data.tobacco_past_use;
			if(data.medical_history) details +=  "<br><br><b>Medical history : </b> "+  data.medical_history;
			if(data.surgical_history) details +=  "<br><b>Surgical history : </b> "+  data.surgical_history;
			if(data.surrounding_factors) details +=  "<br><br><b>Occupational hazards : </b> "+  data.surrounding_factors;
			if(data.other_risk_factors) details += "<br><b>Other risk factors : </b> " + data.other_risk_factors;
			if(data.patient_details) details += "<br><br><b>More info : </b> " + data.patient_details;

			if(details){
				details = "<div style='padding-left:10px; font-size:13px;' align='center'></br><b class='text-muted'>Patient Details</b>" + details + "</div>";
			}

			var vitals = "";
			if(data.temperature) vitals += "<br><b>Temperature :</b> " + data.temperature;
			if(data.pulse) vitals += "<br><b>Pulse :</b> " + data.pulse;
			if(data.respiratory_rate) vitals += "<br><b>Respiratory Rate :</b> " + data.respiratory_rate;
			if(data.bp) vitals += "<br><b>BP :</b> " + data.bp;
			if(data.bmi) vitals += "<br><b>BMI :</b> " + data.bmi;
			if(data.height) vitals += "<br><b>Height :</b> " + data.height;
			if(data.weight) vitals += "<br><b>Weight :</b> " + data.weight;
			if(data.signs_date) vitals += "<br><b>Date :</b> " + data.signs_date;

			if(vitals){
				vitals = "<div style='padding-left:10px; font-size:13px;' align='center'></br><b class='text-muted'>Vital Signs</b>" + vitals + "<br></div>";
				details = vitals + details;
			}
			if(details) details += "<div align='center'><br><a class='btn btn-default btn-sm edit-details'>Edit Details</a></b> </div>";

			me.page.sidebar.addClass("col-sm-3");
			me.page.sidebar.html(details);
			me.page.wrapper.find(".layout-main-section-wrapper").addClass("col-sm-9");
		}
	});
};

var draw_page = function(patient, me){
	frappe.medical_record.last_feed_date = false;
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
			show_filters: false,
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
		var me = this;
		var wrapper = me.page.main.find(".result-list").get(0);
		frappe.medical_record.last_feed_date = false;
		this.page.main.find("div.list-row").remove()
		this.data.map(function (value) {
			var row = $('<div class="list-row" style="clear:both;">').data("data", value).appendTo(me.$result).get(0);
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

	setup_filter_area() {
	}

	setup_sort_selector() {
	}

	setup_list_wrapper() {
		this.page.main.find("div.frappe-list").remove()	
		this.$frappe_list = $('<div class="frappe-list">').appendTo(this.page.main);
	}

	refresh() {
		//this.page.main.find("div.frappe-list").remove()	
		//this.$frappe_list = $('<div class="frappe-list">').appendTo(this.page.main);
		this.freeze(true);

		return frappe.call(this.get_call_args()).then(r => {
			this.prepare_data(r);
			this.toggle_result_area();
			this.before_render();
			this.render();
			this.after_render();
			this.freeze(false);
			if (this.settings && this.settings.refresh) {
				this.settings.refresh(this);
			}
		});
	}
}
