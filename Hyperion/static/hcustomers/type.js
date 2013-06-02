// Document Ready
$(document).ready(function() {
	// check the current selection on page load
	var current_selection = $("#id_primary_type").val();
	toggleAllTypesCheckbox(true, current_selection);

	// associated value change callback
	$("#id_primary_type").change(function() {
		// enable the previously disabled checkbox
		var prev_selection = $("input[name='all_types'][disabled]")
		prev_selection.prop("disabled", false);
		prev_selection.parent().unwrap();

		// check the current selected checkbox
		var current_selection = $(this).val();
		toggleAllTypesCheckbox(true, current_selection);
	});
});

function toggleAllTypesCheckbox(to_check, current_selection) {
	var label_id = "id_all_types_" + current_selection;
	var span = $("label[for='" + label_id + "'] span");
	var input = $("label[for='" + label_id + "'] input");
	if (to_check) {
		span.addClass("checked");
		input.prop("disabled", true);
		input.parent().wrap("<em></em>");
	} else {
		span.removeClass("checked");
	}
}