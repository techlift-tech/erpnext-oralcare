import frappe
import datetime
from frappe.core.doctype.sms_settings.sms_settings import send_sms

@frappe.whitelist()
def get_events(start, end, filters=None):
	appointments = frappe.get_list('Patient Appointment', filters=filters, fields=['patient_name', 'name', 'patient', 'practitioner', 'status', 'duration', 'appointment_date', 'appointment_time'])

	for appointment in appointments:
		patient = appointment.patient
		mobile = ''

		if patient:
			patient_object = frappe.get_doc('Patient', patient)
			if patient_object and patient_object.mobile:
				mobile = patient_object.mobile

		start_date = appointment.appointment_date
		start_timedelta = appointment.appointment_time
		start_time = (datetime.datetime.min + start_timedelta).time()
		appointment.start = datetime.datetime.combine(start_date, start_time) 
		appointment.end = appointment.start + datetime.timedelta(minutes = appointment.duration)
		appointment.color = 'blue'
		appointment.allDay = 0

		appointment.description = '<p style="font-size:20"><i class="fa fa-user-md" aria-hidden="true"></i> %s</p><p style="font-size:20"><i class="fa fa-phone" aria-hidden="true"></i> %s</p>'%(appointment.practitioner, mobile)

	return appointments

def send_doctors_sms(doc, method):
	practitioner = doc.practitioner
	if practitioner:
		doctor = frappe.get_doc('Healthcare Practitioner', practitioner)
		if doctor and doctor.mobile_phone:
			oralcare_settings = frappe.get_doc('Oralcare Settings')
			doc_sms_message = oralcare_settings.doc_appointment_sms
			context = {"doc": doc}
			message = frappe.render_template(doc_sms_message, context)
			numbers = [doctor.mobile_phone]
			send_sms(numbers, message)
