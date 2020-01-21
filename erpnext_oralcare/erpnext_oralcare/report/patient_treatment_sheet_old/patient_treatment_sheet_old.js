// Copyright (c) 2016, Techlift and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Patient Treatment Sheet Old"] = {
	"filters": [
		{
			"fieldname":"date_range",
			"label": __("Date Range"),
			"fieldtype": "DateRange",
			"default": [frappe.datetime.add_months(frappe.datetime.get_today(),-1), frappe.datetime.get_today()],
			"reqd": 1
		},{
			"fieldname":"patient",
			"label": __("Patient"),
			"fieldtype":"Link",
			"options":"Patient"
		},{
			"fieldname":"family_name",
			"label": __("Family Name"),
			"fieldtype":"Link",
			"options":"Family"
		}
	]
}
