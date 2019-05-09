import frappe

def sales_invoice_doctors_share_calculate(doc, method):
	sales_items = doc.items

	for sales_item in sales_items:
		reference_dt = sales_item.reference_dt
		reference_dn = sales_item.reference_dn

		if(reference_dt == 'Clinical Procedure' and reference_dn):

			clinical_procedure = frappe.get_doc('Clinical Procedure', reference_dn)
			if(clinical_procedure):
				doctor = clinical_procedure.practitioner

				if doctor:
					price_list = frappe.get_list('Doctor Pricelist', filters = {'doctor_name': doctor, 'clinical_procedure': clinical_procedure.procedure_template}, fields = ['name', 'sharing_type', 'value'])

					if (price_list and len(price_list) == 1):
						amount = sales_item.amount
						share_value = 0
						qty = sales_item.qty

						if price_list[0].sharing_type == 'percent':
							share_value = (amount * price_list[0].value)/100

						if price_list[0].sharing_type == 'fix':
							share_value = qty*price_list[0].value

						sales_item.doctor_share = share_value

	return
