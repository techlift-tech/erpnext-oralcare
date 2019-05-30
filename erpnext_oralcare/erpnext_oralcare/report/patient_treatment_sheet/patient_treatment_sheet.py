# Copyright (c) 2013, Techlift and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, erpnext
from erpnext.accounts.report.item_wise_sales_register.item_wise_sales_register import get_tax_accounts
import copy
from frappe.utils import flt

billable_healtcare_doctypes = ['Patient Appointment', 'Patient Encounter', 'Lab Test', 'Clinical Procedure', 'Procedure Prescription', 'Lab Prescription']

def execute(filters=None):

	if not filters:
		filters = {}

	from_date = filters.get("date_range")[0]
	to_date = filters.get("date_range")[1]
	patient = filters.get("patient")

	columns, data = [], []

	if patient:
		sales_invoices = frappe.get_list('Sales Invoice', filters = [['posting_date', ">=", from_date], ['posting_date', "<=", to_date], {'patient': patient}])
	else:
		sales_invoices = frappe.get_list('Sales Invoice', filters = [['posting_date', ">=", from_date], ['posting_date', "<=", to_date]])

	columns = [
		'Sales Invoice:Link/Sales Invoice',
		'Date:Date',
		'Procedure:Link/Clinical Procedure',
		'Proceure Name',
		'Doctor:Link/Healthcare Practitioner',
		'Doctor Name',
		'Patient:Link/Patient',
		'Patient Name',
		'Quantity',
		'Rate:Currency',
		'Amount:Currency',
	]

	items_list = []

	for si_name in sales_invoices:
		si = frappe.get_doc('Sales Invoice', si_name)

		if (not si) or (si.docstatus != 1):
			continue

		si_items = si.items

		for item in si_items:
			items_list.append(frappe._dict(vars(item)))

	if  items_list:
		items_tax_list, tax_columns = get_tax_accounts(items_list, columns, 'INR')

		for si_name in sales_invoices:
			si = frappe.get_doc('Sales Invoice', si_name)

			if (not si) or (si.docstatus != 1):
				continue

			posting_date = si.posting_date

			si_items = si.items

			for item in si_items:
				reference_dt = item.reference_dt

				if not reference_dt in billable_healtcare_doctypes:
					continue

				amount = item.amount
				reference_dn = item.reference_dn
				rate = item.rate
				qty = item.qty

				healthcare_doc = frappe.get_doc(reference_dt, reference_dn)

				if healthcare_doc:

					if reference_dt == 'Clinical Procedure' or reference_dt == 'Patient Encounter':
						template =  healthcare_doc.procedure_template if (reference_dt == 'Clinical Procedure') else 'Patient Encounter'
						practitioner = healthcare_doc.practitioner
						patient_id = healthcare_doc.patient

						doctor_name = ''
						doctor_first_name = ''
						if practitioner:
							doctor_name = practitioner
							doctor = frappe.get_doc('Healthcare Practitioner', doctor_name)
							if doctor.first_name:
								doctor_first_name = doctor.first_name

						patient = frappe.get_doc('Patient', patient_id) 
						patient_name = patient.patient_name

						array_to_append = [si_name.name, posting_date, healthcare_doc.name, template, doctor_name, doctor_first_name, patient_id, patient_name, qty, rate, amount]
					elif reference_dt == 'Procedure Prescription' or reference_dt == 'Lab Prescription':
						pass
					else:
						continue

					total_tax = 0
					for tax in tax_columns:
						item_tax = items_tax_list.get(item.name, {}).get(tax, {})
						array_to_append += [item_tax.get("tax_rate", 0), item_tax.get("tax_amount", 0)]
						total_tax += flt(item_tax.get("tax_amount"))

					array_to_append += [total_tax, item.base_net_amount + total_tax, "INR"]

					data.append(array_to_append)

	return columns, data


