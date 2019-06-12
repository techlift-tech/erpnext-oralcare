import frappe

def submit_case_histories(doc, method):
	doctypes = ['General CaseHistory', 'Conservative Dentistry and Endondontics', 'Oral Medicine and Diagnosis', 'Oral Surgery and Trauma', 'Periodontology', 'Prosthodontics', 'Pedodontics']

	for doctype in doctypes:
		open_doctype_names = frappe.get_list(doctype, filters={'encounter': doc.name, 'docstatus': 0})

		for open_doctype_name in open_doctype_names:
			doctype_object = frappe.get_doc(doctype, open_doctype_name)

			if doctype_object:
				doctype_object.submit()

