# Copyright (c) 2013, Techlift and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt

billable_healtcare_doctypes = [
        'Patient Appointment',
        'Patient Encounter',
        'Lab Test',
        'Clinical Procedure',
        'Procedure Prescription',
         'Lab Prescription']


def execute(filters=None):
        columns, data = [], []

        if not filters:
                filters = {}

        from_date = filters.get("date_range")[0]
        to_date = filters.get("date_range")[1]
        doctor_filter = filters.get("doctor")

        columns, data = [], []

        sales_invoices = frappe.get_list(
            'Sales Invoice', filters=[['posting_date', ">=", from_date],
                                      ['posting_date', "<=", to_date]])

        columns = [
                'Invoice:Link/Sales Invoice:90',
                'Date:Date:80',
                'Procedure Name',
                'Doctor Name',
                'Patient Name::150',
                'Value to Dr:Currency',
                'Value to Company:Currency:130',
                'Value to Company(%)'
        ]

        for si_name in sales_invoices:
                si = frappe.get_doc('Sales Invoice', si_name)

                if (not si) or (si.docstatus != 1):
                        continue

                posting_date = si.posting_date

                si_items = si.items

                for item in si_items:
                        reference_dt = item.reference_dt

                        if reference_dt not in billable_healtcare_doctypes:
                                continue

                        reference_dn = item.reference_dn
                        healthcare_procedure = frappe.get_doc(reference_dt, reference_dn)
                        amount = item.amount
                        rate = item.rate
                        qty = item.qty
                        doctor_share = item.doctor_share
                        company_share = amount

                        if reference_dt == 'Clinical Procedure' or reference_dt == 'Patient Encounter':

                                template = healthcare_procedure.procedure_template if(
                                    reference_dt == 'Clinical Procedure') else 'Patient Encounter'
                                practitioner = healthcare_procedure.practitioner
                                patient_id = healthcare_procedure.patient

                                if doctor_filter:
                                        if practitioner != doctor_filter:
                                                continue

                                if doctor_share:
                                        company_share = flt(amount) - flt(doctor_share)
                                        doctor_share = flt(doctor_share)
                                else:
                                        doctor_share = 0

                                if amount == 0:
                                        company_percent = 0
                                else:
                                        company_percent = (company_share/amount)*100

                                doctor_name = ''
                                doctor_name = ''
                                if practitioner:
                                        doctor_name = practitioner
                                        doctor = frappe.get_doc('Healthcare Practitioner', doctor_name)
                                        if doctor.first_name:
                                                doctor_name = doctor.first_name

                                        if doctor.last_name:
                                                doctor_name += " " + doctor.last_name

                                patient = frappe.get_doc('Patient', patient_id)
                                patient_name = patient.patient_name

                                array_to_append = [si_name.name, posting_date, template, doctor_name,
                                                   patient_name, doctor_share, company_share, company_percent]

                                data.append(array_to_append)

        return columns, data
