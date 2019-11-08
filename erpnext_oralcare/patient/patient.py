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


def on_update(doc, method):
	transfer_details_to_customer(doc, method)
	add_customer_address(doc, method)
	

def transfer_details_to_customer(doc, method):
	family_name = doc.family_name
	lead_name = doc.lead_name
	customer = doc.customer
	credit_allowed = doc.credit_allowed

	if customer:
		customer_doc = frappe.get_doc('Customer', customer)
		if customer_doc:
			if family_name:
				customer_doc.family_name = family_name
				customer_doc.save()
			if credit_allowed:
				customer_doc.credit_allowed = credit_allowed
				customer_doc.save()	
			if lead_name:
				customer_doc.lead_name = lead_name
				customer_doc.save()

				lead_doc = frappe.get_doc('Lead', lead_name)

				if lead_doc:
					lead_doc.status = 'Converted'
					lead_doc.save()


def add_customer_address(doc, method):
	customer = doc.customer
	name = doc.name
	address_line1 = doc.address_line1
	address_line2 = doc.address_line2
	city = doc.city
	state = doc.state
	pincode = doc.zip_code
	country = doc.country
	address_name = doc.address_name

	if not address_name:
		if address_line1 and city and country:

			address = frappe.get_doc({
				'doctype': 'Address',
				'address_title': name,
				'address_line1': address_line1,
				'address_line2': address_line2,
				'city': city,
				'state': state,
				'pincode': pincode,
				'country': country,
				'links': [{
					'link_doctype': 'Customer',
					'link_name': customer
				}]
			}).insert()

			if address and address.name:
				doc.address_name = address.name
				doc.save()
	else:
		address = frappe.get_doc('Address', doc.address_name)

		if address:
			address.address_line1 = address_line1
			address.address_line2 = address_line2
			address.city = city
			address.state = state
			address.zip_code = pincode
			address.country = country

			address.save()



