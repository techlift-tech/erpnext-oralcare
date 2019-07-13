from __future__ import unicode_literals
import frappe
from frappe import _
import datetime
import math
from frappe.utils import time_diff_in_hours, rounded, getdate, add_days
from erpnext.healthcare.doctype.healthcare_settings.healthcare_settings import get_income_account
from erpnext.healthcare.doctype.fee_validity.fee_validity import create_fee_validity, update_fee_validity
from erpnext.healthcare.doctype.lab_test.lab_test import create_multiple
from erpnext.healthcare.utils import *

billable_healtcare_doctypes = ['Patient Appointment', 'Patient Encounter', 'Lab Test', 'Clinical Procedure', 'Procedure Prescription', 'Lab Prescription']

def add_accounting_entries(doc, method):
	sales_items = doc.items
	gl_entries = []

	for sales_item in sales_items:
		reference_dt = sales_item.reference_dt
		reference_dn = sales_item.reference_dn
		item_code = sales_item.item_code
		qty = sales_item.qty
		amount = sales_item.amount
		party = None
		gl_amount = 0
		to_do_gl_entry = False

		if reference_dt in billable_healtcare_doctypes and reference_dt:

			healthcare_doc = frappe.get_doc(reference_dt, reference_dn)

			if healthcare_doc:
				if reference_dt == billable_healtcare_doctypes[0]:
					pass
				elif reference_dt == billable_healtcare_doctypes[1]:
					doctor = healthcare_doc.practitioner
					party = doctor
					sales_item.doctor_share = get_doctor_commission(item_code, doctor, qty, amount)
					gl_amount = sales_item.doctor_share
					to_do_gl_entry = True
				elif reference_dt == billable_healtcare_doctypes[2]:
					pass
				elif reference_dt == billable_healtcare_doctypes[3]:
					doctor = healthcare_doc.practitioner
					party = doctor
					sales_item.doctor_share = get_doctor_commission(item_code, doctor, qty, amount)
					gl_amount = sales_item.doctor_share
					to_do_gl_entry = True
				elif reference_dt == billable_healtcare_doctypes[4] or reference_dt == billable_healtcare_doctypes[5]:
					encounter = healthcare_doc.parent
					if encounter:
						encounter_doc = frappe.get_doc(billable_healtcare_doctypes[1], encounter)
						if encounter_doc:
							doctor = encounter_doc.practitioner
							party = doctor
							sales_item.doctor_share = get_doctor_commission(item_code, doctor, qty, amount)
							gl_amount = sales_item.doctor_share
							to_do_gl_entry = True
				else:
					pass

		if to_do_gl_entry:
			oralcare_settings = frappe.get_doc('Oralcare Settings')
			commission_account = oralcare_settings.doctor_commission_payable_accont
			commission_sales_account = oralcare_settings.commission_sales_account
			party_type = oralcare_settings.party_type

			if commission_account and commission_sales_account and party_type:
				gl_entry_debit = doc.get_gl_dict({
					"account": commission_sales_account,
					"debit": gl_amount,
					"debit_in_account_currency": gl_amount,
					"against": party,
					"against_voucher_type": doc.doctype,
					"against_voucher": doc.name,
					"cost_center": sales_item.cost_center
				}, "INR")
				gl_entry_credit = doc.get_gl_dict({
					"account": commission_account,
					"credit": gl_amount,
					"credit_in_account_currency": gl_amount,
					"party_type": party_type,
					"party": party,
					"against": commission_sales_account,
					"against_voucher_type": doc.doctype,
					"against_voucher": doc.name,
					"cost_center": sales_item.cost_center
				}, "INR")

				gl_entries.append(gl_entry_debit)
				gl_entries.append(gl_entry_credit)
			else:
				frappe.throw(_("Please configure Oralcare Settings"))

	if gl_entries:
		from erpnext.accounts.general_ledger import merge_similar_entries
		gl_entries = merge_similar_entries(gl_entries)
		from erpnext.accounts.general_ledger import make_gl_entries
		make_gl_entries(gl_entries, cancel = (doc.docstatus == 2), update_outstanding="No", merge_entries=False)

	return

def sales_invoice_doctors_share_calculate(doc, method):
	sales_items = doc.items

	for sales_item in sales_items:
		reference_dt = sales_item.reference_dt
		reference_dn = sales_item.reference_dn
		item_code = sales_item.item_code
		qty = sales_item.qty
		amount = sales_item.amount

		if reference_dt in billable_healtcare_doctypes and reference_dt:

			healthcare_doc = frappe.get_doc(reference_dt, reference_dn)

			if healthcare_doc:
				if reference_dt == billable_healtcare_doctypes[0]:
					pass
				elif reference_dt == billable_healtcare_doctypes[1]:
					doctor = healthcare_doc.practitioner
					sales_item.doctor_share = get_doctor_commission(item_code, doctor, qty, amount)
				elif reference_dt == billable_healtcare_doctypes[2]:
					pass
				elif reference_dt == billable_healtcare_doctypes[3]:
					doctor = healthcare_doc.practitioner
					sales_item.doctor_share = get_doctor_commission(item_code, doctor, qty, amount)
				elif reference_dt == billable_healtcare_doctypes[4] or reference_dt == billable_healtcare_doctypes[5]:
					encounter = healthcare_doc.parent
					if encounter:
						encounter_doc = frappe.get_doc(billable_healtcare_doctypes[1], encounter)
						if encounter_doc:
							doctor = encounter_doc.practitioner
							sales_item.doctor_share = get_doctor_commission(item_code, doctor, qty, amount)
				else:
					pass

	return

def get_doctor_commission(item_code, doctor, qty, amount):
		share_value = 0
		if doctor:
			commission_price = frappe.get_list('Item Commission List', filters = {'doctor_name': doctor, 'item_code': item_code}, fields = ['commission_type', 'commission_value'])

			if len(commission_price) != 1:
				return share_value

			total_deduction = 0
			deductions = frappe.get_list('Deduction Before Commission', fields = ['deduction_type', 'deduction_value'])
			for deduction in deductions:
				deduction_type = deduction.deduction_type
				deduction_value = deduction.deduction_value

				if deduction_type == 'Percent':
					deduction_to_add = (amount * deduction_value) / 100
					total_deduction += deduction_to_add
				elif deduction_type == 'Fix':
					total_deduction += deduction_value

			item_deductions = frappe.get_list('Item Deduction Before Commission', filters = {'item': item_code}, fields = ['type', 'value'])
			for item_decuction in item_deductions:
				deduction_type = item_decuction.type
				deduction_value = item_decuction.value

				if deduction_type == 'Percent':
					deduction_to_add = (amount * deduction_value) / 100
					total_deduction += deduction_to_add
				elif deduction_type == 'Fix':
					total_deduction += deduction_value

			amount = amount - total_deduction

			if amount > 0:
				commission_type = commission_price[0].commission_type
				commission_value = commission_price[0].commission_value

				if (commission_type and commission_value):
					if commission_type == 'Percent':
						share_value = (amount * commission_value)/100
					elif commission_type == 'Fix':
						share_value = qty*commission_value
			else:
				frappe.throw(_("Final amount after deductions and commission is negative"))

		return share_value

@frappe.whitelist()
def get_healthcare_services(patient):
	patient = frappe.get_doc("Patient", patient)
	if patient:
		if patient.customer:
			item_to_invoice = []
			patient_appointments = frappe.get_list("Patient Appointment",{'patient': patient.name, 'invoiced': False},
			order_by="appointment_date")
			if patient_appointments:
				fee_validity_details = []
				valid_days = frappe.db.get_value("Healthcare Settings", None, "valid_days")
				max_visit = frappe.db.get_value("Healthcare Settings", None, "max_visit")
				for patient_appointment in patient_appointments:
					patient_appointment_obj = frappe.get_doc("Patient Appointment", patient_appointment['name'])

					if patient_appointment_obj.procedure_template:
						pass
					else:
						practitioner_exist_in_list = False
						skip_invoice = False
						if fee_validity_details:
							for validity in fee_validity_details:
								if validity['practitioner'] == patient_appointment_obj.practitioner:
									practitioner_exist_in_list = True
									if validity['valid_till'] >= patient_appointment_obj.appointment_date:
										validity['visits'] = validity['visits']+1
										if int(max_visit) > validity['visits']:
											skip_invoice = True
									if not skip_invoice:
										validity['visits'] = 1
										validity['valid_till'] = patient_appointment_obj.appointment_date + datetime.timedelta(days=int(valid_days))
						if not practitioner_exist_in_list:
							valid_till = patient_appointment_obj.appointment_date + datetime.timedelta(days=int(valid_days))
							visits = 0
							validity_exist = validity_exists(patient_appointment_obj.practitioner, patient_appointment_obj.patient)
							if validity_exist:
								fee_validity = frappe.get_doc("Fee Validity", validity_exist[0][0])
								valid_till = fee_validity.valid_till
								visits = fee_validity.visited
							fee_validity_details.append({'practitioner': patient_appointment_obj.practitioner,
							'valid_till': valid_till, 'visits': visits})

						if not skip_invoice:
							practitioner_charge = 0
							income_account = None
							service_item = None
							if patient_appointment_obj.practitioner:
								service_item, practitioner_charge = service_item_and_practitioner_charge(patient_appointment_obj)
								income_account = get_income_account(patient_appointment_obj.practitioner, patient_appointment_obj.company)
							item_to_invoice.append({'reference_type': 'Patient Appointment', 'reference_name': patient_appointment_obj.name,
							'service': service_item, 'rate': practitioner_charge,
							'income_account': income_account})

			encounters = frappe.get_list("Patient Encounter", {'patient': patient.name, 'invoiced': False, 'docstatus': 1})
			if encounters:
				for encounter in encounters:
					encounter_obj = frappe.get_doc("Patient Encounter", encounter['name'])
					if not encounter_obj.appointment:
						practitioner_charge = 0
						income_account = None
						service_item = None
						if encounter_obj.practitioner:
							service_item, practitioner_charge = service_item_and_practitioner_charge(encounter_obj)
							income_account = get_income_account(encounter_obj.practitioner, encounter_obj.company)

						item_to_invoice.append({'reference_type': 'Patient Encounter', 'reference_name': encounter_obj.name,
						'service': service_item, 'rate': practitioner_charge,
						'income_account': income_account})

			lab_tests = frappe.get_list("Lab Test", {'patient': patient.name, 'invoiced': False})
			if lab_tests:
				for lab_test in lab_tests:
					lab_test_obj = frappe.get_doc("Lab Test", lab_test['name'])
					if frappe.db.get_value("Lab Test Template", lab_test_obj.template, "is_billable") == 1:
						item_to_invoice.append({'reference_type': 'Lab Test', 'reference_name': lab_test_obj.name,
						'service': frappe.db.get_value("Lab Test Template", lab_test_obj.template, "item")})

			procedures = frappe.get_list("Clinical Procedure", {'patient': patient.name, 'invoiced': False})
			if procedures:
				for procedure in procedures:
					procedure_obj = frappe.get_doc("Clinical Procedure", procedure['name'])
					if procedure_obj.procedure_template and (frappe.db.get_value("Clinical Procedure Template", procedure_obj.procedure_template, "is_billable") == 1):
						item_to_invoice.append({'reference_type': 'Clinical Procedure', 'reference_name': procedure_obj.name,
						'service': frappe.db.get_value("Clinical Procedure Template", procedure_obj.procedure_template, "item")})

			procedures = frappe.get_list("Clinical Procedure",
			{'patient': patient.name, 'invoice_separately_as_consumables': True, 'consumption_invoiced': False,
			'consume_stock': True, 'status': 'Completed'})
			if procedures:
				service_item = get_healthcare_service_item('clinical_procedure_consumable_item')
				if not service_item:
					msg = _(("Please Configure {0} in ").format("Clinical Procedure Consumable Item") \
						+ """<b><a href="#Form/Healthcare Settings">Healthcare Settings</a></b>""")
					frappe.throw(msg)
				for procedure in procedures:
					procedure_obj = frappe.get_doc("Clinical Procedure", procedure['name'])
					item_to_invoice.append({'reference_type': 'Clinical Procedure', 'reference_name': procedure_obj.name,
					'service': service_item, 'rate': procedure_obj.consumable_total_amount, 'description': procedure_obj.consumption_details})

			inpatient_services = frappe.db.sql("""select io.name, io.parent from `tabInpatient Record` ip,
			`tabInpatient Occupancy` io where ip.patient=%s and io.parent=ip.name and
			io.left=1 and io.invoiced=0""", (patient.name))
			if inpatient_services:
				for inpatient_service in inpatient_services:
					inpatient_occupancy = frappe.get_doc("Inpatient Occupancy", inpatient_service[0])
					service_unit_type = frappe.get_doc("Healthcare Service Unit Type", frappe.db.get_value("Healthcare Service Unit", inpatient_occupancy.service_unit, "service_unit_type"))
					if service_unit_type and service_unit_type.is_billable == 1:
						hours_occupied = time_diff_in_hours(inpatient_occupancy.check_out, inpatient_occupancy.check_in)
						qty = 0.5
						if hours_occupied > 0:
							actual_qty = hours_occupied / service_unit_type.no_of_hours
							floor = math.floor(actual_qty)
							decimal_part = actual_qty - floor
							if decimal_part > 0.5:
								qty = rounded(floor + 1, 1)
							elif decimal_part < 0.5 and decimal_part > 0:
								qty = rounded(floor + 0.5, 1)
							if qty <= 0:
								qty = 0.5
						item_to_invoice.append({'reference_type': 'Inpatient Occupancy', 'reference_name': inpatient_occupancy.name,
						'service': service_unit_type.item, 'qty': qty})

			return item_to_invoice
		else:
			frappe.throw(_("The Patient {0} do not have customer refrence to invoice").format(patient.name))
