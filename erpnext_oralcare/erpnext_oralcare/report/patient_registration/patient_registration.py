# Copyright (c) 2013, Techlift and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	if not filters:
		filters = {}

	from_date = filters.get("date_range")[0]
	to_date = filters.get("date_range")[1]

	columns, data = [], []

	patient_list = frappe.get_list('Patient', filters = [['creation', ">=", from_date], ['creation', "<=", to_date]])

	columns = [
		'Registration Date: Date',
		'Patient:Link/Patient',
		'Patient Name',
		'Blood Group',
		'Sex',
		'Mobile',
		'Email'
	]

	for patient_id in patient_list:
		patient = frappe.get_doc('Patient', patient_id)
		registration_date = patient.creation
		patient_name = patient.patient_name
		blood_group = patient.blood_group
		sex = patient.sex
		mobile = patient.mobile
		email = patient.email

		data.append([registration_date, patient.name, patient_name, blood_group, sex, mobile, email])

	return columns, data
