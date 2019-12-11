// Copyright (c) 2016, Techlift and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Doctor Financial Report Script"] = {
	"filters": [
		{
			fieldname: "practitioner",
			label: __("Doctor"),
			fieldtype: "Data"
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