import frappe

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

			if commission_account and commission_sales_account:
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
					total_deduction += deduction_value

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

