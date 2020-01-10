// Healthcare
var get_healthcare_services_to_invoice = function(frm) {
	var me = this;
	let selected_patient = '';
	var dialog = new frappe.ui.Dialog({
		title: __("Get Items from Healthcare Services"),
		fields:[
			{
				fieldtype: 'Link',
				options: 'Patient',
				label: 'Patient',
				fieldname: "patient",
				reqd: true
			},
			{ fieldtype: 'Section Break'	},
			{ fieldtype: 'HTML', fieldname: 'results_area' }
		]
	});
	var $wrapper;
	var $results;
	var $placeholder;
	dialog.set_values({
		'patient': frm.doc.patient
	});
	dialog.fields_dict["patient"].df.onchange = () => {
		var patient = dialog.fields_dict.patient.input.value;
		if(patient && patient!=selected_patient){
			selected_patient = patient;
			var method = "erpnext_oralcare.sales_invoice.sales_invoice_extend.get_healthcare_services";
			var args = {patient: patient};
			var columns = (["service", "reference_name", "reference_type"]);
			get_healthcare_items(frm, true, $results, $placeholder, method, args, columns);
		}
		else if(!patient){
			selected_patient = '';
			$results.empty();
			$results.append($placeholder);
		}
	}
	$wrapper = dialog.fields_dict.results_area.$wrapper.append(`<div class="results"
		style="border: 1px solid #d1d8dd; border-radius: 3px; height: 300px; overflow: auto;"></div>`);
	$results = $wrapper.find('.results');
	$placeholder = $(`<div class="multiselect-empty-state">
				<span class="text-center" style="margin-top: -40px;">
					<i class="fa fa-2x fa-heartbeat text-extra-muted"></i>
					<p class="text-extra-muted">No billable Healthcare Services found</p>
				</span>
			</div>`);
	$results.on('click', '.list-item--head :checkbox', (e) => {
		$results.find('.list-item-container .list-row-check')
			.prop("checked", ($(e.target).is(':checked')));
	});
	set_primary_action(frm, dialog, $results, true);
	dialog.show();
};

frappe.ui.form.on("Sales Invoice", {
	customer: function(frm) {
        console.log('hi')
        get_membership_card_and_show(frm)
	}
});

async function get_membership_card_and_show(frm){
    frm.doc.membership_card = ""
    frm.refresh()
    var customer = frm.doc.customer
    var membership_card_allotment = await frappe.db.get_list('Membership Allotment', {filters: {'primary_member': customer}, fields:['name', 'membership_card']})
    if(membership_card_allotment && membership_card_allotment.length == 1){
        var membership_card = membership_card_allotment[0].membership_card
        var membership_card_object = await frappe.db.get_doc('Membership Card', membership_card)
        frm.doc.membership_card = membership_card_object.card_name
        frm.refresh()
    }
}
