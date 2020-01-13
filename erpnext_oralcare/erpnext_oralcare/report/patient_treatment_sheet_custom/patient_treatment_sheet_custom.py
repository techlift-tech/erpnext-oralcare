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
			"width": 180
		},
		{
			"label": "Procedure",
			"fieldtype": "Link",
			"fieldname": "procedure",
			"width": 150,
			"options": "Clinical Procedure"
		},
		{
			"label": "Procedure Name",
			"fieldtype": "Data",
			"fieldname": "item_name",
			"width": 200
		},
		{
			"label": "Doctor Name",
			"fieldtype": "Link",
			"fieldname": "practitioner",
			"width": 250,
			"options": "Healthcare Practitioner"
		},
		{
			"label": "Patient",
			"fieldtype": "Link",
			"fieldname": "patient",
			"width": 150,
			"options": "Patient"
		},
		{
			"label": "Patient Name",
			"fieldtype": "Link",
			"fieldname": "patient_name",
			"width": 150,
			"options": "Customer"
		},
		{
			"label": "Family Name",
			"fieldtype": "data",
			"fieldname": "family_name",
			"width": 150
		},
		{
			"label": "Qty",
			"fieldtype": "data",
			"fieldname": "qty",
			"width": 150
		},
		{
			"label": "Rate",
			"fieldtype": "Currency",
			"fieldname": "rate",
			"width": 100
		},
		{
			"label": "Amt Collected",
			"fieldtype": "Currency",
			"fieldname": "amount",
			"width": 100
		},
		{
			"label": "Total Taxes",
			"fieldtype": "Currency",
			"fieldname": "total_taxes",
			"width": 100
		},
		{
			"label": "Total",
			"fieldtype": "Currency",
			"fieldname": "total",
			"width": 100
		}
		
		
	]

		
def prepare_data(filters):
	cond = cond2 = ""
	if filters.practitioner:
		cond = "and practitioner='{0}'".format(filters.get('practitioner'))
	if filters.family_name:
		cond = "and family_name='{0}'".format(filters.get('family_name'))	
	if filters.start_date and filters.end_date:
		cond2 = "where si.posting_date BETWEEN '{0}' AND '{1}'".format(filters.start_date, filters.end_date)	
	query = """
	select
	si.name as "name",
	DATE_FORMAT(si.posting_date,'%m-%d-%Y') as "posting_date",
	si_item.reference_dn as "procedure",
	si_item.item_name as "item_name",
	si.patient as "patient",
	si.customer_name as "patient_name",
	ifnull(pat.family_name,"N/A") as "family_name",
	case si_item.reference_dt when "Clinical Procedure" 
								then (select practitioner from `tabClinical Procedure` where name = si_item.reference_dn)
								when "Patient Appointment" 
								then (select practitioner from `tabPatient Appointment` where name = si_item.reference_dn)
								 END as "practitioner",
	ifnull(si_item.rate,0) as "rate",
	si_item.amount as "amount",
	si_item.qty as "qty",
	ifnull(si.total_taxes_and_charges,0) as "total_taxes",
	si.grand_total as "total"
	from `tabSales Invoice`as si inner JOIN `tabSales Invoice Item`as si_item on si.name=si_item.parent left join `tabPatient`as pat on si.patient_name=pat.patient_name and si.docstatus=1 having practitioner is not null {1}{0};""".format(cond,cond2)

	frappe.msgprint(query)
	data = frappe.db.sql(query,as_dict=True)
	
	return data