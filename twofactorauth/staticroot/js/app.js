$( document ).ready(function() {
// hide the code field initially
// $('#div_id_code').hide();
// $('#div_id_code').addClass( "hidden" );
// $('#div_id_code').attr("disabled", "disabled");
// $('#id_code').prop( "disabled", true );


// $('#post-form').on('submit', function(event){
//     event.preventDefault();
//     // console.log("preventDefault")
//     signin();
// });
$('#top').text("New header");
$('#auth').click(function(e){
    e.preventDefault();
    signin();    
})​;

$('#verify').click(function(e){
    e.preventDefault();
    verify();    
})​;
// $('#signup-form').on('submit', function(event){
//     event.preventDefault();
//     signup();
// });

// function to signup the user
function signup() {
    $.ajax({
        url : "http://127.0.0.1:8000/signup/", // the endpoint
        type : "POST", // http method
        data : { username: $('#id_username').val(), password1: $('#id_password1').val(), password2: $('#id_password2').val(), phone:$('#id_phone').val() },

        // handle a successful response
        success : function(response) {
        	alert(JSON.stringify(response));
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            alert("error in signup")
        }
    });
};

function signin() {
    $.ajax({
        url : "http://127.0.0.1:8000/login/", // the endpoint
        type : "POST", // http method
        // data : { username: $('#id_username').val(), password: $('#id_password').val(), code: $('#id_code').val(), hidcode:$('#hidcode').val() }, // data sent with the post request
        data : { username: $('#id_username').val(), password: $('#id_password').val(), type_post:'auth' },

        // handle a successful response
        success : function(response) {
        	if (response.mismatch == "no") {
        		// window.location.replace('http://127.0.0.1:8000');
        		switchElements()
        	} else {
        		var error = "<div class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span> The password and username dont match</div>"
        		$('#errors').html(error);
        	}
            // if (response.correct == true && response.mismatch == "no"){
            // 	// alert(JSON.stringify(response));
            // 	window.location.replace('http://127.0.0.1:8000');
            // }else{
            // 	if (response.correct == false) {
            // 		var error = "<div class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span> The code you entered is incorrect</div>"
            // 		$('#errors').html(error);
            // 	} else {
            // 		var error = "<div class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span> The password and username dont match</div>"
            // 		$('#errors').html(error);

            // 	}
            // }
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            alert("error in auth")
        }
    });
};
function switchElements() {
	// hide the top part of the form
	//the username
	$('#div_id_username').addClass( "hidden" );
	$('#id_username').prop( "disabled", true );
	// password
	$('#div_id_password').addClass( "hidden" );
	$('#id_password').prop( "disabled", true );
	// enable the previously disabled code field
	$('#div_id_code').removeClass( "hidden" );
	$('#id_code').prop( "disabled", false );
	// $('input[type="submit"]').prop( "id", "verify" );
	$('input[type="submit"]').val('changed');	
}

function verify() {
	switchElements()
    $.ajax({
        url : "http://127.0.0.1:8000/login/", // the endpoint
        type : "POST", // http method
        data : { code: $('#id_code').val(), hidcode:$('#hidcode').val(), type_post:'verify' },

        // handle a successful response
        success : function(response) {
        	if (response.correct == true) {
        		window.location.replace('http://127.0.0.1:8000');
        	} else if (response.correct == false) {
        		var error = "<div class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span> The code you entered is incorrect</div>"
        		// $('#errors').html('');
        		$('#errors').html(error);
        	}else{
        		var error = "<div class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span> Anonymous error</div>"
        		$('#errors').html(error);
        	}
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            alert("error in verify")
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