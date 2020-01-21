// Copyright (c) 2016, Techlift and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Individual Doctor Data Sheet"] = {
	"filters": [
		{
			"fieldname":"practitioner",
			"label": __("Doctor"),
			"fieldtype":"Link",
			"options":"Healthcare Practitioner",
			"reqd":0
		 },
		{
			fieldname:"start_date",
			label: __("From Date"),
			fieldtype: "Date",
			width: "80"
		},
		{
			fieldname:"end_date",
			label: __("To Date"),
			fieldtype: "Date",
			width: "80"
		}

	]
}
