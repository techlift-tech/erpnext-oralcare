erpnext.LeadController = erpnext.LeadController.extend({
	refresh: function () {
		var doc = this.frm.doc;
		erpnext.toggle_naming_series();
		frappe.dynamic_link = { doc: doc, fieldname: 'name', doctype: 'Lead' }

		if (!doc.__islocal && doc.__onload && !doc.__onload.is_customer) {
			this.frm.add_custom_button(__("Patient"), this.create_patient, __("Make"));
			this.frm.add_custom_button(__("Customer"), this.create_customer, __("Make"));
			this.frm.add_custom_button(__("Opportunity"), this.create_opportunity, __("Make"));
			this.frm.add_custom_button(__("Quotation"), this.make_quotation, __("Make"));
		}

		if (!this.frm.doc.__islocal) {
			frappe.contacts.render_address_and_contact(cur_frm);
		} else {
			frappe.contacts.clear_address_and_contact(cur_frm);
		}
	},
	create_patient: function(){
		frappe.model.open_mapped_doc({
			method: "erpnext_oralcare.lead.lead.make_patient",
			frm: cur_frm
		})
	}
})

$.extend(cur_frm.cscript, new erpnext.LeadController({ frm: cur_frm }));
