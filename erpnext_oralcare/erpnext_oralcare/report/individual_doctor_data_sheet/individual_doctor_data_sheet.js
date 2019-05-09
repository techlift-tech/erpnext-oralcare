// Copyright (c) 2016, Techlift and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Individual Doctor Data Sheet"] = {
	"filters": [
		{
			"fieldname":"date_range",
			"label": __("Date Range"),
			"fieldtype": "DateRange",
			"default": [frappe.datetime.add_months(frappe.datetime.get_today(),-1), frappe.datetime.get_today()],
			"reqd": 1
		},{
			"fieldname":"doctor",
			"label": __("Doctor"),
			"fieldtype":"Link",
			"options":"Healthcare Practitioner"
		}
	]
}
