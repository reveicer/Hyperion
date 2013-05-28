// Document Ready
$(document).ready(function(){
	$("#search_button").click(search);
});


// Search
function search() {
	key = $("#search_text").val();
	if (key) {

		// search companies
		$.ajax({
			type: "GET",
			url: "company/",
			data: {
				key: key
			},
			success: function(data) {
				alert("s");
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
				
			}
		});
	}
}