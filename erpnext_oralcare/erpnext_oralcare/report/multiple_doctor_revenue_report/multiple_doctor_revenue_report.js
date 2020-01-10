// Copyright (c) 2016, Techlift and contributors
// For license information, please see license.txt
/* eslint-disable */

todays_date = frappe.datetime.now().moment
year = todays_date.year()
month = todays_date.month()

frappe.msgprint

year_options = []

for(i = -10; i<= 10; i++){
    year_options.push(year + i)
}

month_options = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
default_month = month_options[month]

frappe.query_reports["Multiple Doctor Revenue Report"] = {
	"filters": [
        {
            "label": "From Year",
            "fieldname": "from_year",
            "fieldtype": "Select",
            "options": year_options,
            "default": year,
            "width": 80
        },
        {
            "label": "From Month",
            "fieldname": "from_month",
            "fieldtype": "Select",
            "options": month_options,
            "default": default_month,
            "width": 80
        },
        {
            "label": "To Year",
            "fieldname": "to_year",
            "fieldtype": "Select",
            "options": year_options,
            "default": year,
            "width": 80
        },
        {
            "label": "To Month",
            "fieldname": "to_month",
            "fieldtype": "Select",
            "options": month_options,
            "default": default_month,
            "width": 80
        },
        {
            "label": "Doctor Type",
            "fieldname": "doctor_type",
            "fieldtype": "Select",
            "options": ["All", "Salaried", "Fixed", "Percent"],
            "default": "All"
        }
	]
}
