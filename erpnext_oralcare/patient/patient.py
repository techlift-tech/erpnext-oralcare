import frappe
from frappe.core.doctype.sms_settings.sms_settings import send_sms

def send_referrer_sms(doc, method):
	referrer_name = doc.referrer_name
	referrer_phone_no = doc.referrer_phone_no
	if referrer_name and referrer_phone_no:
		oralcare_settings = frappe.get_doc('Oralcare Settings')
		referrer_sms_message = oralcare_settings.referrer_sms
		context = {"doc": doc}
		message = frappe.render_template(referrer_sms_message, context)
		numbers = [referrer_phone_no]
		send_sms(numbers, message)

def save_family_name(doc, method):
	family_name = doc.family_name
	customer = doc.customer

	if family_name and customer:
		customer_doc = frappe.get_doc('Customer', customer)
		if customer_doc:
			customer_doc.family_name = family_name
			customer_doc.save()
