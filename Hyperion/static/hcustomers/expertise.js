// Document Ready
$(document).ready(function() {

	var industry_checkboxes = $("input[name='industries']");
	industry_checkboxes.change(function() {
		var span = $(this).next();
		// if unchecked
		if (!span.hasClass("checked")) {
			var value = $(this).val();
			var expertise_counterpart = $("input[name='industry_expertise'][value='" + value + "']");
			var expertise_counterpart_span = expertise_counterpart.next();
			expertise_counterpart_span.removeClass("checked");
		}
	});

	var industry_expertise_checkboxes = $("input[name='industry_expertise']");
	industry_expertise_checkboxes.change(function() {
		var span = $(this).next();
		// if checked
		if (span.hasClass("checked")) {
			var value = $(this).val();
			var industry_counterpart = $("input[name='industries'][value='" + value + "']");
			var industry_counterpart_span = industry_counterpart.next();
			industry_counterpart_span.addClass("checked");
		}
	});

	var category_checkboxes = $("input[name='categories']");
	category_checkboxes.change(function() {
		var span = $(this).next();
		// if unchecked
		if (!span.hasClass("checked")) {
			var value = $(this).val();
			var expertise_counterpart = $("input[name='category_expertise'][value='" + value + "']");
			var expertise_counterpart_span = expertise_counterpart.next();
			expertise_counterpart_span.removeClass("checked");
		}
		
	});

	var category_expertise_checkboxes = $("input[name='category_expertise']")
	category_expertise_checkboxes.change(function() {
		var span = $(this).next();
		// if checked
		if (span.hasClass("checked")) {
			var value = $(this).val();
			var category_counterpart = $("input[name='categories'][value='" + value + "']");
			var category_counterpart_span = category_counterpart.next();
			category_counterpart_span.addClass("checked");
		}
	});
});