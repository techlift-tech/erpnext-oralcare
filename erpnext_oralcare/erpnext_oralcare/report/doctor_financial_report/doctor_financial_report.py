# Copyright (c) 2013, Techlift and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe.permissions import has_permission

billable_healtcare_doctypes = ['Patient Appointment', 'Patient Encounter', 'Lab Test', 'Clinical Procedure', 'Procedure Prescription', 'Lab Prescription']

def execute(filters=None):
	columns, data = [], []

	if not filters:
		filters = {}

	from_date = filters.get("date_range")[0]
	to_date = filters.get("date_range")[1]
	doctor_filter = filters.get("doctor")

	columns, data = [], []

	sales_invoices = frappe.get_list('Sales Invoice', filters = [['posting_date', ">=", from_date], ['posting_date', "<=", to_date]], ignore_permissions=True)

	columns = [
		'Date:Date:80',
		'Patient Name::150',
		'Doctor Name::150',
		'Procedure Name',
		'Amt Collected:Currency',
		'Doctor Share:Currency:130',
		'Admin Fees:Currency:130',
		'Consumable Cost:Currency:130'
	]

	for si_name in sales_invoices:
		si = frappe.get_doc('Sales Invoice', si_name)

		if (not si) or (si.docstatus != 1):
			continue

		posting_date = si.posting_date

		si_items = si.items

		for item in si_items:
			reference_dt = item.reference_dt

			if reference_dt not in billable_healtcare_doctypes:
				continue

			reference_dn = item.reference_dn
			healthcare_procedure = frappe.get_doc(reference_dt, reference_dn)
			amount = item.amount
			doctor_share = item.doctor_share
			admin_fees = item.admin_fees
			consumable_cost = item.consumable_cost

			if reference_dt == 'Clinical Procedure' or reference_dt == 'Patient Encounter':

				template = healthcare_procedure.procedure_template if (reference_dt == 'Clinical Procedure') else 'Patient Encounter'
				patient_id = healthcare_procedure.patient
				practitioner = healthcare_procedure.practitioner

				if doctor_filter:
					if practitioner != doctor_filter:
						continue

				if doctor_share:
					doctor_share = flt(doctor_share)
				else:
					doctor_share = 0

				if admin_fees:
					admin_fees = flt(admin_fees)
				else:
					admin_fees = 0

				if consumable_cost:
					consumable_cost = flt(consumable_cost)
				else:
					consumable_cost = 0

				doctor_name = ''
				if practitioner:
					doctor_list = frappe.get_list('Healthcare Practitioner', fields=['first_name', 'last_name'], filters={'name': practitioner})

					if len(doctor_list) == 0 or len(doctor_list) > 1:
						continue

					doctor_doc = doctor_list[0]

					if doctor_doc.first_name:
						doctor_name = doctor_doc.first_name

						if doctor_doc.last_name:
							doctor_name += " " + doctor_doc.last_name

				patient = frappe.get_doc('Patient', patient_id)
				patient_name = patient.patient_name

				array_to_append = [posting_date, patient_name, doctor_name, template, amount, doctor_share, admin_fees, consumable_cost]

				data.append(array_to_append)

	return columns, data
