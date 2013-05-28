// AJAX CSRF TOKEN
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

// Document Ready
$(document).ready(function() {
    hide_correspondence_error();
    $("#upload_correspondence").click(upload_correspondence);
    $("#records_tab").click(hide_correspondence_error);
});

// Submits the id=correspondence_creation_form form.
// Creates a new correspondence record
function upload_correspondence() {
    content = $("#correspondence_content").val();
    if (content) {
        $.ajax({
            type: "POST",
            url: 'register/correspondence/',
            data: {
                content: $("#correspondence_content").val()
            },
            success: function( json ) {
                // display success message
                // clear & hide post form
                console.log(json);
                insert_correspondence(json);
                $("#records_tab").trigger('click');
            },
            error: function( xhr, status ) {
                show_correspondence_error("Server error. Please try again.");
            },
        });
    } else {
        show_correspondence_error("Message cannot be blank.");
    }
}

function insert_correspondence(record) {
    record_html = ["<div class='row'>", 
                    "<div class='large-6 columns'><p>From: <a href='#'>", record.trader, "</a></p></div>", 
                    "<div class='large-6 columns text-right'>", record.timestamp, "</div>",
                    "<div class='large-12 columns'><p>", record.message, "</p></div>",
                    "<hr/><div>"]
    $("#correspondence_list").prepend(record_html.join(''));
}

function show_correspondence_error(message) {
    error = $("#correspondence_content_error");
    error.html(message);
    error.show();
}

function hide_correspondence_error() {
    error = $("#correspondence_content_error");
    error.html("");
    error.hide();
}