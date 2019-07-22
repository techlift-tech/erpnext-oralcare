frappe.ui.get_print_settings = function (pdf, callback, letter_head) {
	var print_settings = locals[":Print Settings"]["Print Settings"];

	var default_letter_head = locals[":Company"] && frappe.defaults.get_default('company')
		? locals[":Company"][frappe.defaults.get_default('company')]["default_letter_head"]
		: '';

	var columns = [{
		fieldtype: "Check",
		fieldname: "with_letter_head",
		label: __("With Letter head"),
		default: 1
	}, {
		fieldtype: "Select",
		fieldname: "letter_head",
		label: __("Letter Head"),
		depends_on: "with_letter_head",
		options: $.map(frappe.boot.letter_heads, function (i, d) { return d }),
		default: letter_head || default_letter_head
	}, {
		fieldtype: "Select",
		fieldname: "orientation",
		label: __("Orientation"),
		options: "Landscape\nPortrait",
		default: "Landscape"
	}];

	frappe.prompt(columns, function (data) {
		var data = $.extend(print_settings, data);
		if (!data.with_letter_head) {
			data.letter_head = null;
		}
		if (data.letter_head) {
			data.letter_head = frappe.boot.letter_heads[print_settings.letter_head];
		}
		callback(data);
	}, __("Print Settings"));
}
