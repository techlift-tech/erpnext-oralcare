import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_patient(source_name, target_doc=None, ignore_permissions=False):
	doclist = get_mapped_doc("Lead", source_name,
		{"Lead": {
			"doctype": "Patient",
			"field_map": {
				"lead_name": "patient_name",
				"phone": "phone",
				"gender": "sex",
				"date_of_birth": "dob",
				"mobile_no": "mobile",
				"email_id": "email"
			}
		}}, target_doc)

	return doclist
