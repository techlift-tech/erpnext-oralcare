import frappe

billable_healtcare_doctypes = ['Patient Appointment', 'Patient Encounter', 'Lab Test', 'Clinical Procedure', 'Procedure Prescription', 'Lab Prescription']

def add_acocunting_entries(doc, method):
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
					break
				elif reference_dt == billable_healtcare_doctypes[1]:
					doctor = healthcare_doc.practitioner
					sales_item.doctor_share = get_doctor_commission(item_code, doctor, qty, amount)
					break
				elif reference_dt == billable_healtcare_doctypes[2]:
					break
				elif reference_dt == billable_healtcare_doctypes[3]:
					doctor = healthcare_doc.practitioner
					sales_item.doctor_share = get_doctor_commission(item_code, doctor, qty, amount)
					break
				elif reference_dt == billable_healtcare_doctypes[4] or reference_dt == billable_healtcare_doctypes[5]:
					encounter = healthcare_doc.parent
					if encounter:
						encounter_doc = frappe.get_doc(billable_healtcare_doctypes[1], encounter)
						if encounter_doc:
							doctor = encounter_doc.practitioner
							sales_item.doctor_share = get_doctor_commission(item_code, doctor, qty, amount)
					break
				else:
					break

	return

def get_doctor_commission(item_code, doctor, qty, amount):
		if doctor:
			commission_price_list = frappe.get_list('Item Commission List', filters = {'doctor_name': doctor, 'item_code': item_code})
			share_value = 0

			if len(commission_price_list) != 1:
				return 0

			commission_price = frappe.get_doc('Item Commission List', commission_price_list[0])

			total_deduction = 0
			deductions = frappe.get_list('Deduction Before Commission')
			for deduction_name in deductions:
				deduction = frappe.get_doc('Deduction Before Commission', deduction_name.name)
				deduction_type = deduction.deduction_type
				deduction_value = deduction.deduction_value

				if deduction_type == 'Percent':
					deduction_to_add = (amount * deduction_value) / 100
					total_deduction += deduction_to_add
				elif deduction_type == 'Fix':
					total_deduction += deduction_valued

			amount = amount - total_deduction

			if amount > 0:
				commission_type = commission_price.commission_type
				commission_value = commission_price.commission_value

				if (commission_type and commission_value):
					if commission_type == 'Percent':
						share_value = (amount * commission_value)/100
					elif commission_type == 'Fix':
						share_value = qty*commission_value

		return share_value

