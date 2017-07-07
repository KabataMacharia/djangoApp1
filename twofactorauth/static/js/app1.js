$( document ).ready(function() {
    // hide the code field on the signin form
	$('#div_id_code').addClass( "hidden" );
	$('#id_code').prop( "disabled", true );

    // $("h3").text("context")

    $('#auth').click(function(e) {
        e.preventDefault();
    	signin();
    });

    $('#signup-form').on('submit', function(event){
        event.preventDefault();
        signup();
    });

    function signup() {
    $.ajax({
        url : "http://127.0.0.1:8000/signup/", // the endpoint
        type : "POST", // http method
        xhrFields: {
        withCredentials: true
    },
        data : { username: $('#id_username').val(),email: $('#id_email').val(), password1: $('#id_password1').val(), password2: $('#id_password2').val(), phone:$('#id_phone').val(), is_staff:$('#id_is_staff').val(), is_superuser:$('#id_is_superuser').val(), is_admin:$('#id_is_admin').val() },

        // handle a successful response
        success : function(response) {
            
            if (response.registered == "yes") {
                window.location.replace('http://127.0.0.1:8000');
            } else {
                var error = "";
                $.each(response, function(key, errorvalue) {
                    console.log(key);
                    console.log(errorvalue);
                    if (key == "password2") {
                        errorvalue.forEach(function(element) {
                            // console.log(element);
                            error += "<p class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span>"+element+"</p>";
                        });
                    } else {
                        var errorvalue=errorvalue[0];
                        // console.log( errorvalue);
                        error += "<p class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span>"+errorvalue+"</p>";
                    }                  
                });
                // if (typeof(response.exists) != "undefined") {
                //     error += "<p class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span>The phone number must be unique</p>";
                // } 
                // display the errors
                 $('#errors').html(error);
            }
            
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error in signup");
        }
    });
	};

	function signin() {
    $.ajax({
        url : "http://127.0.0.1:8000/login/", // the endpoint
        type : "POST", // http method
        xhrFields: {
        withCredentials: true
        },
        data : {csrfmiddlewaretoken: csrftoken, username: $('#id_username').val(), password: $('#id_password').val(), type_post:'auth' },

        // handle a successful response
        success : function(response) {
        	if (response.mismatch == "no") {
        		switchElements()
        	} else {
        		var error = "<div class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span> The password and username dont match</div>"
        		$('#errors').html(error);
        	}
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error in auth");
	        }
	    });
	};

	function switchElements() {
	// hide the top part of the form
	//the username
    $('#errors').html( "" );
	$('#div_id_username').addClass( "hidden" );
	$('#id_username').prop( "disabled", true );
	// password
	$('#div_id_password').addClass( "hidden" );
	$('#id_password').prop( "disabled", true );
	// enable the previously disabled code field
	$('#div_id_code').removeClass( "hidden" );
	$('#id_code').prop( "disabled", false );
    $('input[type="submit"]').replaceWith('<input class="btn btn-block btn-primary" id="verify" type="submit" name="button" value="verify code"/>');
	}

    $(document).on('click','#verify',(function(e) {
        e.preventDefault();
        $.ajax({
        url : "http://127.0.0.1:8000/login/",
        type : "POST", // http method
        xhrFields: {
        withCredentials: true
        },
        data : { csrfmiddlewaretoken: csrftoken, code: $('#id_code').val(),  type_post:'verify' },

        // handle a successful response
        success : function(response) {
        	if (response.correct == true) {
        		window.location.replace('http://127.0.0.1:8000');
                // console.log('hello2');
        	} else if (response.correct == false) {
        		var error = "<div class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span> The code you entered is incorrect</div>";
        		$('#errors').html(error);
        	}else{
        		var error = "<div class='alert alert-danger' role='alert'><span class='glyphicon glyphicon-exclamation-sign' aria-hidden='true'></span> <span class='sr-only'>Error:</span> Anonymous error</div>";
        		$('#errors').html(error);
        	}
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error in verify");
            }
            });
        }));



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