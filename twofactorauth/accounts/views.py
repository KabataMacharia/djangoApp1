from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
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

	# user_entered_verify_code = raw_input("Please enter the verification code you were sent: ")

	# if verify_code == user_entered_verify_code.strip():
	#     print("Your code is correct.")
	# else:
	#     print("Your code is incorrect.")

# @login_required
def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.phone = form.cleaned_data.get('phone')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            # sendOTP()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# def signin(request):
# 	if request.method == 'POST':

# 		form = SignInForm(request.POST)
# 		if form.is_valid:
# 			username = request.POST['username']
# 			password = request.POST['password']
# 			code = request.POST['code']
# 			send_code = request.POST['hidcode']

# 			# username = "otp"
# 			# password = "1234pass"
# 			# code = "123wq"
# 			# username = form.cleaned_data.get('username')
# 			# password = form.cleaned_data.get('password') 
# 			# code  = form.cleaned_data.get('code')
# 			if code.strip() == send_code:
# 				user = authenticate( username=username, password=password)
# 				if user is not None:
# 					login(request, user)
# 					return redirect('home')
# 				else:
# 					return render(request, 'mismatched_credentials.html',)
# 			else:
# 				return render(request, 'bad_code.html', {})
# 	else:
# 		form = SignInForm()
# 		customer_id = "A7A625FD-AFE4-4E3D-AE51-DEBF9CCAA1BA"
# 		api_key = "DuhC8MQ71NO89g2eamglt64gNN31+luy0TShI4zXn6K5OEbNRf98FSC5lmUPr5pf7zZNJlKzooY0b60hki4fKQ=="

# 		phone_number = "+254702029382"
# 		verify_code = random_with_n_digits(5)
# 		message = "Your code is {}".format(verify_code)
# 		message_type = "OTP"

# 		messaging = MessagingClient(customer_id, api_key)
# 		response = messaging.message(phone_number, message, message_type)
# 		# sendOTP()
# 		return render(request, 'login.html', {'form':form,"code":verify_code})

def signin(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		code = request.POST.get('code')
		hidcode = request.POST.get('hidcode')
		response_data = {}
		correct = False

		response_data['username'] = username
		response_data['code'] = code
		response_data['hidcode'] = hidcode
		response_data['password'] = password
		response_data['correct'] = correct
		if code == hidcode:
			correct = True
			response_data['correct'] = correct
			user = authenticate( username=username, password=password)
			if user is not None:
				login(request, user)
				# return redirect('home')
				response_data['mismatch'] = 'no'
				return JsonResponse(response_data)

			else:
				response_data['mismatch'] = 'yes'
				return JsonResponse(response_data)
				# return JsonResponse({"bad password": "They are not matching"})
		else:
			return JsonResponse(response_data)
			# return JsonResponse({"bad code": "no matching code"})
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
		# sendOTP()
		return render(request, 'login.html', {'form':form,"code":verify_code})
		# return JsonResponse({"nothing to see": "this isn't happening"})
	else:
		return redirect('home')