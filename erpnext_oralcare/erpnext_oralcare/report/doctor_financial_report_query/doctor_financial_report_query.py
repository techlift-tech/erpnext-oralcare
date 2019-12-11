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
			"width": 180,
			"options": ""
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
			"width": 200,
			"options": ""
		},
		{
			"label": "Amt Collected",
			"fieldtype": "Currency",
			"fieldname": "amount",
			"width": 100,
			"options": ""
		},
		{
			"label": "Doctor Share",
			"fieldtype": "Currency",
			"fieldname": "doctor_share",
			"width": 100,
			"options": ""
		},
		{
			"label": "Admin Fees",
			"fieldtype": "Currency",
			"fieldname": "admin_fees",
			"width": 100,
			"options": ""
		},
		{
			"label": "Consumable Cost",
			"fieldtype": "Currency",
			"fieldname": "consumable_cost",
			"width": 100,
			"options": ""
		},
		{
			"label": "Reference Doctype",
			"fieldtype": "Data",
			"fieldname": "reference_dt",
			"width": 100,
			"options": ""
		},
		{
			"label": "Reference Name",
			"fieldtype": "Data",
			"fieldname": "reference_dn",
			"width": 100,
			"options": ""
		},
		
	]

		
def prepare_data(filters):
	cond = cond2 = ""
	if filters.practitioner:
		cond = "AND cp.practitioner= '{0}'".format(filters.get('practitioner')) 
	if filters.start_date and filters.end_date:
		cond2 = "AND si.posting_date BETWEEN '{0}' AND '{1}'".format(filters.start_date, filters.end_date)
	query = """
	SELECT 
		si.name,
		si_item.parent,
		DATE_FORMAT(si.posting_date,'%m-%d-%Y') as "posting_date",
		si.customer_name as "customer_name",
		IF(si_item.reference_dt="Clinical Procedure",(select practitioner from `tabClinical Procedure` where name=si_item.reference_dn),(select practitioner from `tabPatient Appointment` where name=si_item.reference_dn)) as "practitioner",
		si_item.item_name as "item_name",
		si_item.amount as "amount",
		si_item.reference_dt as "reference_dt",
		si_item.reference_dn as "reference_dn",
		si_item.doctor_share as "doctor_share",
		si_item.admin_fees as "admin_fees",
		si_item.consumable_cost as "consumable_cost"
	FROM`tabSales Invoice Item` as si_item
	 INNER JOIN `tabSales Invoice` as si on si_item.parent = si.name
	 LEFT JOIN  `tabPatient Appointment` as ap on si_item.reference_dn=ap.name
	 LEFT JOIN `tabClinical Procedure` as cp on si_item.reference_dn=cp.name where (si_item.reference_dt="Clinical Procedure" OR si_item.reference_dt="Patient Appointment"){0} {1}
		;""".format(cond,cond2)
	# -- print(query)
	data = frappe.db.sql(query,as_dict=True)
	
	return data
