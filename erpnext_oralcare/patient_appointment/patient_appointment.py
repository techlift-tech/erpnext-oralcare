import frappe
import datetime
from frappe.core.doctype.sms_settings.sms_settings import send_sms

@frappe.whitelist()
def get_events(start, end, filters=None):
	appointments = frappe.get_list('Patient Appointment', filters=filters, fields=['name', 'patient', 'practitioner', 'status', 'duration', 'appointment_date', 'appointment_time'])

	for appointment in appointments:
		start_date = appointment.appointment_date
		start_timedelta = appointment.appointment_time
		start_time = (datetime.datetime.min + start_timedelta).time()
		appointment.start = datetime.datetime.combine(start_date, start_time) 
		appointment.end = appointment.start + datetime.timedelta(minutes = appointment.duration)
		appointment.color = 'blue'
		appointment.allDay = 0
		appointment.description = "Dr: " + appointment.practitioner

	return appointments

def send_doctors_sms(doc, method):
	oralcare_settings = frappe.get_doc('Oralcare Settings')
	doc_sms_message = oralcare_settings.doc_appointment_sms
	send_sms(doc, doc_sms_message)
	pass
