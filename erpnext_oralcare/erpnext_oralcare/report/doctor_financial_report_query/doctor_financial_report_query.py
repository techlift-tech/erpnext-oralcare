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
			"fieldtype": "Data",
			"fieldname": "amount",
			"width": 100,
			"options": ""
		},
		{
			"label": "Doctor Share",
			"fieldtype": "Data",
			"fieldname": "doctor_share",
			"width": 100,
			"options": ""
		},
		{
			"label": "Admin Fees",
			"fieldtype": "Data",
			"fieldname": "admin_fees",
			"width": 100,
			"options": ""
		},
		{
			"label": "Consumable Cost",
			"fieldtype": "Data",
			"fieldname": "consumable_cost",
			"width": 100,
			"options": ""
		},
		
	]

		
def prepare_data(filters):
	query = """
	SELECT 
		si.name,
		si_item.parent,
		si.posting_date as "posting_date",
		si.customer_name as "customer_name",
		cp.practitioner as "practitioner",
		si_item.item_name as "item_name",
<<<<<<< Updated upstream:erpnext_oralcare/erpnext_oralcare/report/doctor_financial_report_query/doctor_financial_report_query.py
		si_item.amount as amount,
=======
		si_item.amount as "amount",
		si_item.reference_dt as "reference_dt",
		si_item.reference_dn as "reference_dn",
>>>>>>> Stashed changes:erpnext_oralcare/erpnext_oralcare/report/doctor_financial_report_script/doctor_financial_report_script.py
		si_item.doctor_share as "doctor_share",
		si_item.admin_fees as "admin_fees",
		si_item.consumable_cost as "consumable_cost"
	FROM`tabSales Invoice Item` as si_item
	 INNER JOIN `tabSales Invoice` as si on si_item.parent = si.name
	 LEFT JOIN `tabClinical Procedure` as cp on si_item.reference_dn=cp.name
		;"""
	# -- print(query)
	data = frappe.db.sql(query,as_dict=True)
	
	return data
