from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    phone = forms.CharField(help_text='Your phone number')

    class Meta:
        model = User
        fields = ('username', 'phone', 'password1', 'password2', )

class SignInForm(AuthenticationForm):
	code = forms.CharField()
	class Meta:
		model = User
		fields = ('username', 'password', )
		# widgets = {
  #           'username': forms.TextInput(
  #               attrs={'id': 'username', 'required': True, 'placeholder': 'username'}
  #           ),
  #           'password': forms.PasswordInput(
  #               attrs={'id': 'password', 'required': True, 'placeholder': 'password'}
  #           ),
  #           'code': forms.TextInput(
  #               attrs={'id': 'code', 'required': True, 'placeholder': 'code'}
  #           ),
  #       }

# class SignInForm(ModelForm):
# 	# code = forms.CharField()
# 	class Meta:
# 		model = User
# 		fields = ('username', 'password', )

# from django.forms import ModelForm

# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email')

# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         fields = ('phone')