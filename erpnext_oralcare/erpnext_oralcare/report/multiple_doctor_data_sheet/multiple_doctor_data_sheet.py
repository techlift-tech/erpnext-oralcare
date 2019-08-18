# Copyright (c) 2013, Techlift and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import datetime
from frappe.utils import flt
import json

billable_healtcare_doctypes = ['Patient Appointment', 'Patient Encounter', 'Lab Test', 'Clinical Procedure', 'Procedure Prescription', 'Lab Prescription']

def execute(filters=None):
	columns, data, columns_new = [], [], []

	if not filters:
		filters = {}

	from_date = filters.get("date_range")[0]
	to_date = filters.get("date_range")[1]

	column_prefixes = [{'title':'Value to Dr', 'type':'Currency'}, {'title':'Value to Co.', 'type':'Currency'}, {'title':'Value to Co. in%', 'type':'Int'}]

	if from_date and to_date:

		doctor_filter = filters.get("doctor")

		from_date_datetime = datetime.datetime.strptime(from_date, "%Y-%m-%d")
		to_date_datetime = datetime.datetime.strptime(to_date, "%Y-%m-%d")

		from_year = from_date_datetime.year
		to_year = to_date_datetime.year

		from_month = from_date_datetime.month
		to_month = to_date_datetime.month

		for year in range(from_year, to_year + 1):
			start_month = 1
			end_month = 12
			if year == from_year:
				start_month = from_month
			if year == to_year:
				end_month = to_month

			for month in range(start_month, end_month + 1):
				month_name = datetime.date(1900, month, 1).strftime('%B')
				month_name = month_name[:3]
				for prefix_json in column_prefixes:
					prefix = prefix_json['title']
					column_json = {
						'title': prefix_json['title'] + " " + str(month_name) + " " + str(year),
						'type': prefix_json['type'],
					}
					columns.append(column_json)

	sales_invoices = frappe.get_list('Sales Invoice', filters = [['posting_date', ">=", from_date], ['posting_date', "<=", to_date]])

	doctors_month_wise_share = {}

	for si_name in sales_invoices:
		si = frappe.get_doc('Sales Invoice', si_name)

		if (not si) or (si.docstatus != 1):
			continue

		posting_date = si.posting_date
		year = posting_date.year
		month_name = posting_date.strftime('%B')
		month_name = month_name[:3]

		si_items = si.items

		for item in si_items:
			reference_dt = item.reference_dt

			if reference_dt not in billable_healtcare_doctypes:
				continue

			reference_dn = item.reference_dn
			healthcare_doc = frappe.get_doc(reference_dt, reference_dn)
			amount = item.amount
			rate = item.rate
			qty = item.qty
			doctor_share = item.doctor_share
			company_share = amount
			practitioner = None

			if reference_dt == 'Clinical Procedure' or reference_dt == 'Patient Encounter':
				practitioner = healthcare_doc.practitioner
			elif reference_dt == 'Procedure Prescription' or reference_dt == 'Lab Prescription':
				encounter = healthcare_doc.parent
				if encounter:
					encounter_doc = frappe.get_doc('Patient Encounter', encounter)
					if encounter_doc:
						practitioner = encounter_doc.practitioner
			else:
				continue

			if practitioner:
				if doctor_filter:
					if practitioner != doctor_filter:
						continue

				if doctor_share:
					company_share = flt(amount) - flt(doctor_share)
					doctor_share = flt(doctor_share)
				else:
					doctor_share = 0.0

				if practitioner:
					doctor_id = practitioner
					if doctor_id not in doctors_month_wise_share:
						doctors_month_wise_share[doctor_id] = {}

					month_year_key = month_name + " " + str(year)

					if month_year_key not in doctors_month_wise_share[doctor_id]:
						doctors_month_wise_share[doctor_id][month_year_key] = {
							'self': 0.0,
							'co': 0.0
						} 

					doctors_month_wise_share[doctor_id][month_year_key]['self'] += doctor_share
					doctors_month_wise_share[doctor_id][month_year_key]['co'] += company_share

	for doctor_id in doctors_month_wise_share:
		temp_rate = {}
		temp_data = [doctor_id]

		for column_json in columns:
			temp_rate[column_json['title']] = 0.0

		for month in doctors_month_wise_share[doctor_id]:
			self_amount = doctors_month_wise_share[doctor_id][month]['self']
			co_amount = doctors_month_wise_share[doctor_id][month]['co']
			co_percent = (co_amount*100)/(co_amount + self_amount)

			temp_rate[column_prefixes[0]['title'] + " " + month] = self_amount
			temp_rate[column_prefixes[1]['title'] + " " + month] = co_amount
			temp_rate[column_prefixes[2]['title'] + " " + month] = co_percent

		for column_json in columns:
			column_title = column_json['title']
			temp_data.append(temp_rate[column_title])

		data.append(temp_data)

		columns_new = ['Doctor Name']
		for column_json in columns:
			field_type = column_json['type']
			title = column_json['title']
			if field_type == 'Currency':
				title += ":Currency"
			columns_new.append(title)

	return columns_new, data
