frappe.views.calendar['Patient Appointment'] = {
	options: {
		header: {
			right: 'prev,today,next month,agendaWeek,agendaDay,listWeek',
		},
		defaultView: 'listWeek',
		eventStartEditable: false,
		disableDragging: true,
		editable: false,
		slotDuration: '00:15:00',
		slotLabelInterval: 15,
		slotLabelFormat: 'h(:mm)a',
		slotMinutes: 15,
		disableResizing: true,
		minTime: "09:00:00",
		maxTime: "21:00:00",
		hiddenDays: [0],
		noEventsMessage: "No Appointments to Show",
		selectable: false,
		nowIndicator: false
	},
	field_map: {
		"start": "start",
		"end": "end",
		"id": "name",
		"title": "patient_name",
		"allDay": "allDay",
		"eventColor": "color",
		"description": "description",
		"tooltip": "description"
	},
	order_by: "appointment_date",
	gantt: true,
	get_events_method: "erpnext_oralcare.patient_appointment.patient_appointment.get_events"
}
