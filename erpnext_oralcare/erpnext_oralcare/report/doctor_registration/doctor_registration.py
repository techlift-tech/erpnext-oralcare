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

	doctor_list = frappe.get_list('Healthcare Practitioner', filters = [['creation', ">=", from_date], ['creation', "<=", to_date]])

	columns = [
		'Registration Date: Date:150',
		'Doctor:Link/Healthcare Practitioner:150',
		'Doctor Name::150',
		'Department::250',
		'Designation:Link/Designation:150',
		'Mobile::150'
	]

	for doctor_id in doctor_list:
		doctor = frappe.get_doc('Healthcare Practitioner', doctor_id)
		registration_date = doctor.creation
		first_name = doctor.first_name
		last_name = doctor.last_name
		mobile = doctor.mobile_phone
		designation = doctor.designation
		department = doctor.department

		doctor_name = ''

		if first_name:
			doctor_name += first_name

		if last_name:
			doctor_name += " " + last_name

		if designation == None:
			designation = 'N/A'

		print(type(designation))

		data.append([registration_date, doctor.name, doctor_name, department, designation, mobile])

	return columns, data
