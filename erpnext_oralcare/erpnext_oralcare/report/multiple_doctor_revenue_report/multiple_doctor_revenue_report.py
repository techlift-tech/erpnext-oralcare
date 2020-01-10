# Copyright (c) 2013, Techlift and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import calendar


def execute(filters=None):
    columns, data = [], []
    data = prepare_data(filters)
    columns = get_columns(filters)
    return columns, data


def get_columns(filters=None):
    return [
        {
            "label": "Type",
            "fieldname": "TYPE",
            "fieldtype": "Data",
            "width": 60
        },
        {
            "label": "DOCTOR",
            "fieldname": "DOCTOR"
        },
        {
            "label": "AMT COLLECTED",
            "fieldname": "SUM OF AMT COLLECTED",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": "CONSUMABLE COST",
            "fieldname": "SUM OF CONSUMABLE COST",
            "fieldtype": "Currency"
        },
        {
            "label": "ADMIN FEES",
            "fieldname": "SUM OF ADMIN FEES",
            "fieldtype": "Currency"
        },
        {
            "label": "DOCTOR SHARE",
            "fieldname": "SUM OF DOCTOR SHARE",
            "fieldtype": "Currency"
        },
        {
            "label": "COMPANY SHARE",
            "fieldname": "COMPANY SHARE",
            "fieldtype": "Currency"
        },
        {
            "label": "%",
            "fieldname": "%",
            "fieldtype": "Data",
            "width": 60
        },

    ]


def prepare_data(filters):
    month_options = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    from_year = filters.from_year
    to_year = filters.to_year
    from_month = filters.from_month
    to_month = filters.to_month

    from_month_digit = "{0:0=2d}".format(month_options.index(from_month) + 1)
    to_month_digit = "{0:0=2d}".format(month_options.index(to_month) + 1)

    from_date = "%s-%s-%s"%(from_year, from_month_digit, "01")

    to_date_last_date = calendar.monthrange(int(to_year), month_options.index(to_month) + 1)[1]
    to_date = "%s-%s-%s"%(to_year, to_month_digit, to_date_last_date)

    from_date_object = frappe.utils.datetime.datetime.strptime(from_date, "%Y-%m-%d")
    to_date_object = frappe.utils.datetime.datetime.strptime(to_date, "%Y-%m-%d")

    if(from_date_object > to_date_object):
        frappe.msgprint("From Date Cannot be Greater Than To Date")
        return []

    doctor_condition = ""
    doctor_type = filters.doctor_type

    if(doctor_type != "All"):
        doctor_condition = "and b.doctor_type = '%s'"%(doctor_type)

    query = """SELECT *, (d.`SUM OF AMT COLLECTED` - d.`SUM OF CONSUMABLE COST` - d.`SUM OF DOCTOR SHARE` - d.`SUM OF ADMIN FEES`) AS "COMPANY SHARE",
        ROUND(( 100 * (d.`SUM OF AMT COLLECTED` - d.`SUM OF CONSUMABLE COST` - d.`SUM OF DOCTOR SHARE` - d.`SUM OF ADMIN FEES`) / d.`SUM OF AMT COLLECTED`), 2) AS "%"
        from (Select doctor_type as TYPE, dr as DOCTOR, amt as "SUM OF AMT COLLECTED", cons as "SUM OF CONSUMABLE COST", adm as "SUM OF ADMIN FEES",
        CASE WHEN c.doctor_type = "Salaried" THEN (SELECT IFNULL(sum(net_pay),0) from `tabSalary Slip` where employee = c.employee and start_date BETWEEN "{0}" and "{1}" and docstatus = 1) ELSE c.`share/salary` END "SUM OF DOCTOR SHARE" from (select a.*, b.mobile_phone,b.employee,
        CASE WHEN b.doctor_type = "Salaried" THEN "Salaried" WHEN b.doctor_type = "Fixed" THEN "Fixed" WHEN b.doctor_type = "Percent" THEN "percent"
        ELSE "none" END as doctor_type from (select parent, IFNULL(SUM(amount),0) as amt, IFNULL(SUM(admin_fees),0) as adm, IFNULL(SUM(consumable_cost),0) as cons,
        IFNULL(SUM(doctor_share),0) as "share/salary", CASE WHEN reference_dt = "Patient Appointment" THEN (select practitioner from `tabPatient Appointment`
        where name = reference_dn) when reference_dt = "Clinical Procedure" then (select practitioner from `tabClinical Procedure` where name = reference_dn) END as dr
        from `tabSales Invoice Item` GROUP BY dr HAVING dr is NOT NULL) as a LEFT JOIN `tabHealthcare Practitioner` as b ON a.dr = b.name LEFT JOIN `tabSales Invoice` as
        si ON a.parent = si.name where si.posting_date BETWEEN "{0}" and "{1}" and si.docstatus = 1 {2}) as c) as d""".format(from_date, to_date, doctor_condition)
    #frappe.msgprint(query)
    data = frappe.db.sql(query)
    return data
