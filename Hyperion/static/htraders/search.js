// Document Ready
$(document).ready(function(){
	$("#search-button").click(search);
	company_results_container = $("#company-results");
	company_results_list = $("#company-results ol")
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
		var item = $("<a/>").attr("href", "/profile/company/"+company.id+"/").html(company.name);
		company_results_list.append($("<li>").html(item));
	});
}

function load_contact_results(contacts) {
	contact_results_list.html("");
	$.each(contacts, function(i) {
		contact = contacts[i];
		var item = $("<a/>").attr("href", "/profile/contact/"+contact.id+"/").html(contact.first_name + " " + contact.last_name).appendTo($("<li/>"));
		contact_results_list.append(item);
	});
}