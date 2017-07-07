from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
# from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import User
from .decorators import admin_member_required,superuser_member_required,staff_member_required
# imports for class based views
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

# telesign imports
from telesign.messaging import MessagingClient
from telesign.util import random_with_n_digits
# from telesign.api import Verify

from .forms import SignInForm,SignUpForm

# customer_id = "A7A625FD-AFE4-4E3D-AE51-DEBF9CCAA1BA"
# secret_key = "DuhC8MQ71NO89g2eamglt64gNN31+luy0TShI4zXn6K5OEbNRf98FSC5lmUPr5pf7zZNJlKzooY0b60hki4fKQ=="
# user_verification = Verify(customer_id, secret_key)

# phone_info = user_verification.sms("+254702029382", use_case_code="ATCK")
# user_entered_verifycode = "3456"
# status_info = user_verification.status(phone_info.data["reference_id"],
#     verify_code=user_entered_verifycode)
# if status_info.data["verify"]["code_state"] == 'VALID':
# 	pass
@staff_member_required
def staff_view(request):
	return render(request, 'staff.html')

@admin_member_required
def admin_view(request):
	return render(request, 'admin.html')

@superuser_member_required
def super_user_view(request):
	return render(request, 'superuser.html')
@login_required
def not_allowed(request):
    return render(request, 'not_member.html')

@login_required
def home(request):
    return render(request, 'home.html')
# class based view for home
class home(LoginRequiredMixin,TemplateView):
	template_name = 'home.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

def signup(request):	
    if request.method == 'POST':
    	form = SignUpForm(request.POST)
    	# this is for the form validations
    	cleaned_password = form.clean_password()
    	cleaned_phone = form.clean_phone()
    	cleaned_email = form.clean_email()

    	if (type(cleaned_password) == dict):
    		form.add_error(None, cleaned_password)
    	if (type(cleaned_email) == dict):
    		form.add_error(None, cleaned_email)

    	if form.is_valid():
    		# role = request.POST.get('your_role')
    		is_staff = request.POST.get('is_staff')
    		is_superuser = request.POST.get('is_superuser')
    		is_admin = request.POST.get('is_admin')

    		user = form.save()
    		raw_password = form.cleaned_data.get('password1')
    		username = form.cleaned_data.get('username')
    		user.set_password(raw_password)
    		if int(is_staff) == 2:
    			user.is_staff = True
    		else:
    			user.is_staff = False

    		if int(is_admin) == 2:
    			user.is_staff = True
    			user.is_admin = True
    		else:
    			user.is_admin = False

    		if int(is_superuser) == 2:
    			user.is_staff = True
    			user.is_admin = True
    			user.is_superuser = True
    		else:
    			user.is_superuser = False
    		user.save()
    		user = authenticate(username = username, password=raw_password)    		
    		login(request, user)

    		response_data = {}
    		response_data['registered'] = "yes"
    		return JsonResponse(response_data)
    	else:
    		response_data = {}
    		response_data['registered'] = "no"
    		# response_data['role'] = request.POST.get('your_role')
    		response_data['is_staff'] = request.POST.get('is_staff')
    		response_data['is_superuser'] = request.POST.get('is_superuser')
    		response_data['is_admin'] = request.POST.get('is_admin')
    		return JsonResponse(form.errors)
    elif request.user.is_authenticated():
    	return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})
# @ensure_csrf_cookie
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
				# store user details after auth
				request.session['username'] = username
				request.session['password'] = password
				# user = User.objects.get(username=username)
				# phone_number = user.phone
				
				customer_id = "A7A625FD-AFE4-4E3D-AE51-DEBF9CCAA1BA"
				api_key = "DuhC8MQ71NO89g2eamglt64gNN31+luy0TShI4zXn6K5OEbNRf98FSC5lmUPr5pf7zZNJlKzooY0b60hki4fKQ=="

				phone_number = "+254702029382"
				verify_code = random_with_n_digits(5)
				message = "Your code is {}".format(verify_code)
				message_type = "OTP"

				messaging = MessagingClient(customer_id, api_key)
				response = messaging.message(phone_number, message, message_type)
				request.session['code'] = verify_code
				# verify_code = 65432
				# request.session['code'] = verify_code
				response_data['mismatch'] = 'no'
				return JsonResponse(response_data)
			#the user doesnt have correct credentials
			else:
				response_data['mismatch'] = 'yes'
				return JsonResponse(response_data)
		# this will happen after the user has been authenticated
		elif request_type == 'verify':
			# if processing the code, get it and the hidden one
			code = request.POST.get('code')
			# hidcode = request.POST.get('hidcode')
			code = code.strip()
			# code = int(code)
			hidcode = request.session['code']

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
		return render(request, 'login.html', {'form':form})
	else:
		return redirect('home')
