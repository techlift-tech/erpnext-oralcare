from __future__ import unicode_literals
from frappe import _

def get_data():

	return [
		{
			"label": _("Consultation"),
			"icon": "icon-star",
			"items": [
				{
					"type": "doctype",
					"name": "Patient Appointment",
					"label": _("Patient Appointment"),
				},
				{
					"type": "doctype",
					"name": "Patient Encounter",
					"label": _("Patient Encounter"),
				},
				{
					"type": "doctype",
					"name": "Vital Signs",
					"label": _("Vital Signs"),
					"description": _("Record Patient Vitals"),
				},
				{
					"type": "page",
					"name": "medical_record",
					"label": _("Patient Medical Record"),
				},
				{
					"type": "page",
					"name": "appointment-analytic",
					"label": _("Appointment Analytics"),
				},
				{
					"type": "doctype",
					"name": "Clinical Procedure",
					"label": _("Clinical Procedure"),
				}
			]
		},
		{
			"label": _("Reports"),
			"icon": "icon-star",
			"items": [
				{
					"type": "report",
					"is_query_report": True,
					"name": "Doctor Financial Report",
					"label": _("Doctor Financial Report")
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Doctor Registration",
					"label": _("Doctor Registration")
				},
				{
					"type": "report",
					"name": "Doctor Value",
					"is_query_report": True,
					"label": _("Doctor Value")
				},
				{
					"type": "report",
					"name": "Individual Patient Data Sheet",
					"is_query_report": True,
					"label": _("Individual Patient Data Sheet")
				},
				{
					"type": "report",
					"name": "Individual Doctor Data Sheet",
					"is_query_report": True,
					"label": _("Individual Doctor Data Sheet")
				},
				{
					"type": "report",
					"name": "Multiple Doctor Data Sheet",
					"is_query_report": True,
					"label": _("Multiple Doctor Data Sheet")
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "Patient Treatment Sheet",
					"label": _("Patient Treatment Sheet")
				},
				{
					"is_query_report": True,
					"type": "report",
					"name": "Patient Registration",
					"label": _("Patient Registartion")
				},
				{
					"type": "report",
					"is_query_report": True,
					"name": "General Ledger Oralcare",
					"label": "General Ledger Oralcare"
				}

			]
		},
		{
			"label": _("Masters"),
			"icon": "icon-list",
			"items": [
				{
					"type": "doctype",
					"name": "Patient",
					"label": _("Patient"),
				},
				{
					"type": "doctype",
					"name": "Healthcare Practitioner",
					"label": _("Healthcare Practitioner"),
				},
				{
					"type": "doctype",
					"name": "Practitioner Schedule",
					"label": _("Practitioner Schedule"),
				},
				{
					"type": "doctype",
					"name": "Medical Code Standard",
					"label": _("Medical Code Standard"),
				},
				{
					"type": "doctype",
					"name": "Medical Code",
					"label": _("Medical Code"),
				}
			]
		},
		{
			"label": _("Setup"),
			"icon": "icon-cog",
			"items": [
				{
					"type": "doctype",
					"name": "Healthcare Settings",
					"label": _("Healthcare Settings"),
				},
				{
					"type": "doctype",
					"name": "Medical Department",
					"label": _("Medical Department"),
				},
				{
					"type": "doctype",
					"name": "Appointment Type",
					"label": _("Appointment Type"),
				},
				{
					"type": "doctype",
					"name": "Prescription Dosage",
					"label": _("Prescription Dosage")
				},
				{
					"type": "doctype",
					"name": "Prescription Duration",
					"label": _("Prescription Duration")
				},
				{
					"type": "doctype",
					"name": "Complaint",
					"label": _("Complaint")
				},
				{
					"type": "doctype",
					"name": "Diagnosis",
					"label": _("Diagnosis")
				},
				{
					"type": "doctype",
					"name": "Antibiotic",
					"label": _("Antibiotic")
				},
				{
					"type": "doctype",
					"name": "Sensitivity",
					"label": _("Sensitivity")
				},
				{
					"type": "doctype",
					"name": "Clinical Procedure Template",
					"label": _("Clinical Procedure Template"),
				}
			]
		},
		{
			"label": _("Case History"),
			"icon": "icon-cog",
			"items": [
				{
					"type": "doctype",
					"name": "General CaseHistory",
					"label": _("General CaseHistory"),
				},
				{
					"type": "doctype",
					"name": "Conservative Dentistry and Endondontics",
					"label": _("Conservative Dentistry and Endondontics"),
				},
				{
					"type": "doctype",
					"name": "Oral Medicine and Diagnosis",
					"label": _("Oral Medicine and Diagnosis"),
				},
				{
					"type": "doctype",
					"name": "Oral Surgery and Trauma",
					"label": _("Oral Surgery and Trauma")
				},
				{
					"type": "doctype",
					"name": "Periodontology",
					"label": _("Periodontology")
				},
				{
					"type": "doctype",
					"name": "Prosthodontics",
					"label": _("Prosthodontics")
				},
				{
					"type": "doctype",
					"name": "Pedodontics",
					"label": _("Pedodontics")
				}
			]
		}

	]

