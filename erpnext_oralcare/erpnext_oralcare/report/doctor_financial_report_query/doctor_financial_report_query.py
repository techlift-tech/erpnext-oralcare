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
			"label": "Date",
			"fieldtype": "Data",
			"fieldname": "posting_date",
			"width": 180
		},
		{
			"label": "Patient Name",
			"fieldtype": "Link",
			"fieldname": "customer_name",
			"width": 150,
			"options": "Customer"
		},
		{
			"label": "Doctor Name",
			"fieldtype": "Link",
			"fieldname": "practitioner",
			"width": 250,
			"options": "Healthcare Practitioner"
		},
		{
			"label": "Procedure Name",
			"fieldtype": "Data",
			"fieldname": "item_name",
			"width": 200
		},
		{
			"label": "Amt Collected",
			"fieldtype": "Currency",
			"fieldname": "amount",
			"width": 100
		},
		{
			"label": "Doctor Share",
			"fieldtype": "Currency",
			"fieldname": "doctor_share",
			"width": 100
		},
		{
			"label": "Admin Fees",
			"fieldtype": "Currency",
			"fieldname": "admin_fees",
			"width": 100
		},
		{
			"label": "Consumable Cost",
			"fieldtype": "Currency",
			"fieldname": "consumable_cost",
			"width": 100
		}				
	]		
def prepare_data(filters):
	cond = cond2 = ""
	if filters.practitioner:
		cond = "having practitioner='{0}'".format(filters.get('practitioner'))
	if filters.start_date and filters.end_date:
		cond2 = "where si.posting_date BETWEEN '{0}' AND '{1}'".format(filters.start_date, filters.end_date)	
	query = """
	select
	si.name as "name",
	DATE_FORMAT(si.posting_date,'%d-%m-%Y') as "posting_date",
	si.customer_name as "customer_name",
	case si_item.reference_dt when "Clinical Procedure"
			then (select practitioner from `tabClinical Procedure` where name = si_item.reference_dn)
			when "Patient Appointment" 
			then (select practitioner from `tabPatient Appointment` where name = si_item.reference_dn) 
			else "other" END as "practitioner",
	si_item.item_name as "item_name",
	si_item.amount as "amount",
	si_item.doctor_share as "doctor_share",
	si_item.admin_fees as "admin_fees",
	si_item.consumable_cost as "consumable_cost",
	si_item.reference_dt as "reference_dt",
	si_item.reference_dn as "reference_dn"
	from `tabSales Invoice Item` as si_item LEFT JOIN `tabSales Invoice` as si on si_item.parent = si.name and si.docstatus=1 {1}{0};""".format(cond,cond2)

	data = frappe.db.sql(query,as_dict=True)
	
	return data