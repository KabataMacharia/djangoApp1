from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.http import JsonResponse


# telesign imports
from telesign.messaging import MessagingClient
from telesign.util import random_with_n_digits

from .forms import SignUpForm,SignInForm

# function to send otp
def sendOTP():
	customer_id = "A7A625FD-AFE4-4E3D-AE51-DEBF9CCAA1BA"
	api_key = "DuhC8MQ71NO89g2eamglt64gNN31+luy0TShI4zXn6K5OEbNRf98FSC5lmUPr5pf7zZNJlKzooY0b60hki4fKQ=="

	phone_number = "+254702029382"
	verify_code = random_with_n_digits(5)
	message = "Your code is {}".format(verify_code)
	message_type = "OTP"

	messaging = MessagingClient(customer_id, api_key)
	response = messaging.message(phone_number, message, message_type)

@login_required
def home(request):
    return render(request, 'home.html')

def signup(request):	
    if request.method == 'POST':
    	username = request.POST.get('username')
    	phone = request.POST.get('phone')
    	password1 = request.POST.get('password1')
    	password2 = request.POST.get('password2')
    	response_data = {}
    	response_data['username'] = username
    	response_data['password1'] = password1
    	response_data['password2'] = password2
    	response_data['phone'] = phone
    	# try:
    	# 	user = User.objects.create_user(username, 'lennon@thebeatles.com', '1234pass')
    	# 	user.refresh_from_db()
    	# 	user.profile.phone = phone
    	# 	user.save()
    	# 	raw_password = password1
    	# 	user = authenticate(username=username, password=raw_password)
    	# 	login(request, user)
    	# 	response_data['registered'] = "yes"
    	# 	return JsonResponse(response_data)
    	# except:
    	# 	response_data['registered'] = "no"
    	# 	return JsonResponse(response_data)
    	# User.objects.create_user("tom", 'lennon@thebeatles.com', '1234pass')
    	# user = User.objects.create_user(username, 'lennon@thebeatles.com', '1234pass')
    	# if user is not None:
    	# 	user.refresh_from_db()
    	# 	user.profile.phone = '+254702029382'
    	# 	user.save()
    	# 	raw_password = password1
    	# 	user = authenticate(username=username, password=raw_password)
    	# 	login(request, user)
    	# 	response_data['registered'] = "yes"
    	# 	return JsonResponse(response_data)
    	# else:
    	# 	response_data['registered'] = "no"
    	# 	return JsonResponse(response_data)

    	# make the data to bind to the form
    	formdata = {'username':username,'phone':phone,'password1':password1,'password2':password2}
    	form = SignUpForm(formdata)
    	# form = SignUpForm(request.POST)
    	if form.is_valid():
    		# user = User(username=username, password1=password1, password2=password2)
    		# user.save()
    		# user.profile.phone = phone
    		# raw_password = password1
 
    		user = form.save()
    		user.refresh_from_db()  # load the profile instance created by the signal
    		user.profile.phone = form.cleaned_data.get('phone')
    		user.save()
    		raw_password = form.cleaned_data.get('password1')
    		user = authenticate(username=user.username, password=raw_password)
    		login(request, user)

    		response_data = {}
    		response_data['username'] = username
    		response_data['password'] = password1
    		response_data['registered'] = "yes"
    		return JsonResponse(response_data)
    	else:
    		# return redirect('home')
    		response_data = {}
    		response_data['username'] = username
    		response_data['password'] = password1
    		response_data['registered'] = "no"
    		# return JsonResponse(response_data)
    		return JsonResponse(form.errors)
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

def signin(request):
	if request.method == 'POST':
		# get the part of the form being processed
		request_type = 'verify'
		request_type = request.POST.get('type_post')
		if request_type == 'auth':
			# if first part, get the username and password
			username = request.POST.get('username')
			password = request.POST.get('password')

			# make a dictionary of responses for json
			response_data = {}
			response_data['username'] = username
			response_data['password'] = password

			# check to make sure the user exists and credentials match
			user = authenticate( username=username, password=password)
			if user is not None:
				# login the user after auth
				request.session['username'] = username
				request.session['password'] = password
				# login(request, user)
				response_data['mismatch'] = 'no'
				return JsonResponse(response_data)
			#the user doesnt have correct credentials
			else:
				response_data['mismatch'] = 'yes'
				return JsonResponse(response_data)
		elif request_type == 'verify':
			# if processing the code, get it and the hidden one
			code = request.POST.get('code', 0)
			hidcode = request.POST.get('hidcode', 0)

			# code = 1
			# hidcode = 1
			# make a dictionary of responses for json
			response_data = {}
			correct = False
			response_data['code'] = code
			response_data['hidcode'] = hidcode
			response_data['correct'] = correct
			# return JsonResponse(response_data)

			# determine if the user entered is correct

			if code == hidcode:
				# login(request, user)
				correct = True
				response_data['correct'] = correct
				username = request.session['username']
				password = request.session['password']
				user = authenticate( username=username, password=password)
				login(request, user)

				return JsonResponse(response_data)
			else:
				return JsonResponse(response_data)
	elif request.method == 'GET' and not  request.user.is_authenticated():
		form = SignInForm()
		# customer_id = "A7A625FD-AFE4-4E3D-AE51-DEBF9CCAA1BA"
		# api_key = "DuhC8MQ71NO89g2eamglt64gNN31+luy0TShI4zXn6K5OEbNRf98FSC5lmUPr5pf7zZNJlKzooY0b60hki4fKQ=="

		# phone_number = "+254702029382"
		# verify_code = random_with_n_digits(5)
		# message = "Your code is {}".format(verify_code)
		# message_type = "OTP"

		# messaging = MessagingClient(customer_id, api_key)
		# response = messaging.message(phone_number, message, message_type)
		verify_code = 65432
		return render(request, 'login.html', {'form':form,"code":verify_code})
	else:
		return redirect('home')