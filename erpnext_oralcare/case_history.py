import frappe

def insert_case_history_in_medical_record(doc, method):
	subject = "Case History Entry"

	medical_record = frappe.new_doc("Patient Medical Record")
	medical_record.patient = doc.patient
	medical_record.subject = subject
	medical_record.status = "Open"
	medical_record.reference_doctype = doc.doctype
	medical_record.reference_name = doc.name
	medical_record.reference_owner = doc.owner
	medical_record.save(ignore_permissions=True)
