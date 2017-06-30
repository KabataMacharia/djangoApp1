$( document ).ready(function() {

$('#post-form').on('submit', function(event){
    event.preventDefault();
    signin();
});

function signin() {
    $.ajax({
        url : "http://127.0.0.1:8000/login/", // the endpoint
        type : "POST", // http method
        data : { username: $('#id_username').val(), password: $('#id_password').val(), code: $('#id_code').val(), hidcode:$('#hidcode').val() }, // data sent with the post request

        // handle a successful response
        success : function(response) {
            // alert(JSON.stringify(json)); // log the returned json to the console
            // window.location.replace('http://127.0.0.1:8000/');
            // alert("success");
            if (response.correct == true && response.mismatch == "no"){
            	// alert(JSON.stringify(response));
            	window.location.replace('http://127.0.0.1:8000');
            }else{
            	// var error = "<P>the error</p>"
            	if (response.correct == false) {
            		var error = "<div class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span> The code you entered is incorrect</div>"
            		$('#errors').html(error);
            	} else {
            		var error = "<div class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span> The password and username dont match</div>"
            		$('#errors').html(error);

            	}
            	// var error = "<div class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span> Enter a valid email address</div>"

            	// window.location.replace('http://127.0.0.1:8000/login/');
            	// $('#errors').html("<div class="alert alert-danger" role="alert"><span class="glyphicon glyphicon-exclamation-sign" aria-hidden="true"></span> <span class="sr-only">Error:</span> Enter a valid email address</div>"); 
            	
            	// $( '#errors' ).replaceWith( "<h2>New heading</h2>" );
            	// alert("your username or password is incorect");
            }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            // $('#errors').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            //     " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            // alert(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            alert("error")
        }
    });
};

// This function gets cookie with a given name
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
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
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

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});