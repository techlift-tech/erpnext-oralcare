import datetime
from dateutil.relativedelta import *
import frappe
from frappe.utils import cint, today, formatdate

def get_healthcare_doctypes():
	billable_healtcare_doctypes = ['Patient Appointment', 'Patient Encounter', 'Lab Test', 'Clinical Procedure', 'Procedure Prescription', 'Lab Prescription']
	return billable_healtcare_doctypes

def get_daily_sales(posting_date, company):
	results = frappe.db.sql('''
		select
			sum(base_grand_total) as total
		from
			`tabSales Invoice`
		where
			posting_date="{0}"
			and docstatus = 1
			and company = "{1}"
	'''.format(posting_date, frappe.db.escape(company)), as_dict = True)

	total = results[0]['total'] if len(results) > 0 else 0

	if total == None:
		total = 0

	return total

def get_todays_sale():
	return get_daily_sales(today(), "Oralcare.co.in")

def get_month_sale(month_year_string, company):
	results = frappe.db.sql('''
		select
			sum(base_grand_total) as total, date_format(posting_date, '%m-%Y') as month_year
		from
			`tabSales Invoice`
		where
			date_format(posting_date, '%m-%Y')="{0}"
			and docstatus = 1
			and company = "{1}"
		group by
			month_year
	'''.format(month_year_string, frappe.db.escape(company)), as_dict = True)

	monthly_total = results[0]['total'] if len(results) > 0 else 0

	return monthly_total

def get_last_month_sale():
	last_month = datetime.datetime.now() - relativedelta(months=1)
	last_month_string = last_month.strftime("%m-%Y")

	return get_month_sale(last_month_string, "Oralcare.co.in")

def get_current_month_sale():
	current_month = datetime.datetime.now()
	current_month_string = current_month.strftime("%m-%Y")

	return get_month_sale(current_month_string, "Oralcare.co.in")


def send_daily_sales_sms():
	oralcare_settings = frappe.get_doc('Oralcare Settings')

	if not oralcare_settings:
		return
	if not oralcare_settings.number_for_sales_report:
		return
	if oralcare_settings.number_for_sales_report == '':
		return

	number_arrays = oralcare_settings.number_for_sales_report.split(',')

	from frappe.core.doctype.sms_settings.sms_settings import send_sms
	todays_sale = get_todays_sale()
	current_month_sale = get_current_month_sale()
	last_month_sale = get_last_month_sale()
	message = '''Today's Sale: {0} .\nMonth Till Date: {1} .\nLast Month: {2}'''.format(todays_sale, current_month_sale, last_month_sale)
	try:
		send_sms(number_arrays, message)
	except e:
		pass

def send_daily_appointment_summary():
    todays_date = today()
    tomorrows_date = frappe.utils.add_days(todays_date, 1)
    appointments = frappe.get_all('Patient Appointment', fields=['name', 'practitioner', 'appointment_time', 'patient_name'], filters={'appointment_date': tomorrows_date}, order_by='appointment_time')

    doctor_wise_apppointment = {}
    for appointment in appointments:
        doctor = appointment.practitioner

        if doctor not in doctor_wise_apppointment:
            doctor_wise_apppointment[doctor] = []

        doctor_wise_apppointment[doctor].append(appointment)

    from frappe.core.doctype.sms_settings.sms_settings import send_sms

    for doctor in doctor_wise_apppointment:
        doctor_object = frappe.get_doc('Healthcare Practitioner', doctor)
        if doctor_object:
            mobile_number = doctor_object.mobile_phone
            if mobile_number:
                summary_message = '''Your Appointments for Tomorrow {0} \n'''.format(frappe.utils.formatdate(tomorrows_date, 'dd-MM-YY'))
                for appointment in doctor_wise_apppointment[doctor]:
                    summary_message += '''{0}-{1}\n'''.format(appointment.appointment_time, appointment.patient_name)

                if summary_message != '':
                    summary_message = summary_message.replace('`', '')
                    summary_message = summary_message.replace('@', '')
                    summary_message = summary_message.replace('&', '')
                    summary_message = summary_message.replace('#', '')
                    send_sms([mobile_number], summary_message)

