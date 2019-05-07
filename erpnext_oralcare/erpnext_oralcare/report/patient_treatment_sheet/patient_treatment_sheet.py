# Copyright (c) 2013, Techlift and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, erpnext
from erpnext.accounts.report.item_wise_sales_register.item_wise_sales_register import get_tax_accounts
import copy
from frappe.utils import flt

def execute(filters=None):

	if not filters:
		filters = {}

	from_date = filters.get("date_range")[0]
	to_date = filters.get("date_range")[1]

	columns, data = [], []

	sales_invoices = frappe.get_list('Sales Invoice', filters = [['posting_date', ">=", from_date], ['posting_date', "<=", to_date]])

	columns = [
		'Sales Invoice:Link/Sales Invoice',
		'Date:Date',
		'Procedure:Link/Clinical Procedure',
		'Proceure Name',
		'Doctor:Link/Healthcare Practitioner',
		'Doctor Name',
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

	items_tax_list, tax_columns = get_tax_accounts(items_list, columns, 'INR')

	for si_name in sales_invoices:
		si = frappe.get_doc('Sales Invoice', si_name)

		if (not si) or (si.docstatus != 1):
			continue

		posting_date = si.posting_date

		si_items = si.items

		for item in si_items:
			reference_dt = item.reference_dt

			if not reference_dt == 'Clinical Procedure':
				continue

			amount = item.amount
			reference_dn = item.reference_dn
			rate = item.rate
			qty = item.qty

			clinical_procedure = frappe.get_doc('Clinical Procedure', reference_dn)
			template = clinical_procedure.procedure_template
			practitioner = clinical_procedure.practitioner

			doctor_name = ''
			doctor_first_name = ''
			if practitioner:
				doctor_name = practitioner
				doctor = frappe.get_doc('Healthcare Practitioner', doctor_name)
				if doctor.first_name:
					doctor_first_name = doctor.first_name

			array_to_append = [si_name.name, posting_date, clinical_procedure.name, template, doctor_name, doctor_first_name, qty, rate, amount]

			total_tax = 0
			for tax in tax_columns:
				item_tax = items_tax_list.get(item.name, {}).get(tax, {})
				array_to_append += [item_tax.get("tax_rate", 0), item_tax.get("tax_amount", 0)]
				total_tax += flt(item_tax.get("tax_amount"))

			array_to_append += [total_tax, item.base_net_amount + total_tax, "INR"]

			data.append(array_to_append)

	return columns, data


