# Copyright (c) 2013, Techlift and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute(filters=None):
	data = prepare_data(filters)
	columns = get_columns(filters)
	return columns, data

def get_columns(filters=None):
	return [
		{
			"label": "Name",
			"fieldtype": "Link",
			"fieldname": "name",
			"width": 100,
			"options": "Sales Invoice"
		},
		{
			"label": "Date",
			"fieldtype": "Data",
			"fieldname": "posting_date",
			"width": 180,
			"options": ""
		},
		{
			"label": "Procedure Name",
			"fieldtype": "Data",
			"fieldname": "item_name",
			"width": 200,
			"options": ""
		},
		{
			"label": "Doctor Name",
			"fieldtype": "Link",
			"fieldname": "practitioner",
			"width": 250,
			"options": "Healthcare Practitioner"
		},
		{
			"label": "Patient Name",
			"fieldtype": "Link",
			"fieldname": "patient_name",
			"width": 150,
			"options": "Customer"
		},
		{
			"label": "Amt Collected",
			"fieldtype": "Currency",
			"fieldname": "amount",
			"width": 100,
			"options": ""
		},
		{
			"label": "Value to Doctor",
			"fieldtype": "Currency",
			"fieldname": "doctor_share",
			"width": 100,
			"options": ""
		},
		{
			"label": "Value to Company",
			"fieldtype": "Currency",
			"fieldname": "value_to_company",
			"width": 100,
			"options": ""
		}
		
		
	]

		
def prepare_data(filters):
	date_cond = practitioner_cond = ""
	if filters.practitioner:
		practitioner_cond = "and practitioner='{0}'".format(filters.get('practitioner'))
	if filters.start_date and filters.end_date:
		date_cond  = "where si.posting_date BETWEEN '{0}' AND '{1}'".format(filters.start_date, filters.end_date)	
	query = """
	select
	si.name as "name",
	DATE_FORMAT(si.posting_date,'%d-%m-%Y') as "posting_date",
	si_item.item_name as "item_name",
	si.customer_name as "patient_name",
	case si_item.reference_dt when "Clinical Procedure" 
	then (select practitioner from `tabClinical Procedure` where name = si_item.reference_dn)
	when "Patient Appointment" 
	then (select practitioner from `tabPatient Appointment` where name = si_item.reference_dn)
	END as "practitioner",
	ifnull(si_item.doctor_share,0) as "doctor_share",
	si_item.amount as "amount",ifnull(si_item.amount-si_item.doctor_share,0) as "value_to_company" 
	from `tabSales Invoice`as si inner JOIN `tabSales Invoice Item`as si_item on si.name=si_item.parent and si.docstatus=1 {0} having practitioner is not null {1};""".format(date_cond,practitioner_cond)

	data = frappe.db.sql(query,as_dict=True)
	
	return data
