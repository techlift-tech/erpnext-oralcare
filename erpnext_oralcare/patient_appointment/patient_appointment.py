import frappe
import datetime

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

	return appointments


