// Document Ready
$(document).ready(function(){
	$("#search-button").click(search);
	company_results_container = $("#company-results");
	company_results_list = $("#company-results ul")
	contact_results_container = $("#contact-results");
	contact_results_list = $("#contact-results ul")
});


// Search
function search() {
	var key = $("#search_text").val();
	if (key) {
		// search companies
		$.ajax({
			type: "GET",
			url: "company/",
			data: {
				key: key
			},
			success: function(data) {
				load_company_results(data);
			}
		});

		// search contacts
		$.ajax({
			type: "GET",
			url: "contact/",
			data: {
				key: key
			},
			success: function(data) {
				load_contact_results(data);	
			}
		});
	}
}

function load_company_results(companies) {
	company_results_list.html("");
	$.each(companies, function(i) {
		company = companies[i];
		var item = $("<a/>").attr("href", "/profile/company/"+company.id+"/").html(company.name).appendTo($("<li/>"));
		company_results_list.append(item);
	});
}

function load_contact_results(data) {
	contact_results_list.html("");
	$.each(contacts, function(i) {
		contact = contacts[i];
		var item = $("<a/>").attr("href", "/profile/contact/"+contact.id+"/").html(contact.name).appendTo($("<li/>"));
		contact_results_list.append(item);
	});
}