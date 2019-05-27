frappe.ui.form.on('Kanban Board', 'reference_doctype', function(frm){
	if(!frm.doc.reference_doctype || !frm.doc.board_based_on) return;

	frappe.model.with_doctype(frm.doc.reference_doctype, function() {
		var options = $.map(frappe.get_meta(frm.doc.reference_doctype).fields,
			function(d) {
				if(d.fieldname && d.fieldtype === frm.doc.board_based_on &&
					frappe.model.no_value_type.indexOf(d.fieldtype)===-1) {
					return d.fieldname;
				}
				return null;
			});
		frm.set_df_property('field_name', 'options', options);
		frm.get_field('field_name').refresh();
	});

	doctype = frappe.get_meta(frm.doc.reference_doctype)
	var fields_to_add = []
	for(var field of doctype.fields){
		if(field.in_list_view == 1) {
			fields_to_add.push(field.fieldname)	
		}
	}
	frappe.meta.get_docfield('Kanban Board Card Fields', 'field', frm.docname).options = fields_to_add
})
frappe.ui.form.on('Kanban Board', 'field_type', function(frm){
	var field = frappe.meta.get_field(frm.doc.reference_doctype, frm.doc.field_name);
	frm.doc.columns = [];
	if(frm.doc.board_based_on == 'Select') {
		field.options && field.options.split('\n').forEach(function(o) {
			o = o.trim();
			if(!o) return;
			var d = frm.add_child('columns');
			d.column_name = o;
		});
	} else if(frm.doc.board_based_on == 'Date') {
		var d = frm.add_child('columns');
		d.column_name = 'Today';
		var d = frm.add_child('columns');
		d.column_name = 'Tomorrow';
		var d = frm.add_child('columns');
		d.column_name = 'Day After Tomorrow';
		var d = frm.add_child('columns');
		d.column_name = 'Other';
	}
	frm.refresh();
})
