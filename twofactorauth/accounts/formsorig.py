from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import ModelForm
# from django.contrib.auth.models import User
# from .models import Profile
from .models import User
from django.core import validators
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# for ensuring the phone number is unique
def validate_phone(value):
  if User.objects.filter(phone=value).exists():
    raise ValidationError("This phone number:"+value+" is already used ")

class SignUpForm(UserCreationForm):
    # phone = forms.CharField(help_text='Your phone number',validators=[validate_phone,RegexValidator('^[0-9]{10}$', message="phone number should be 10 digits")])
    phone = forms.CharField(help_text='Your phone number',validators=[RegexValidator('^[0-9]{10}$', message="phone number should be 10 digits")])

    class Meta:
        model = User
        fields = ('username','email', 'phone', 'password1', 'password2', )
    def save(self, commit=True):
      if not commit:
        raise NotImplementedError("Can't create User and UserProfile without database save")
      user = super().save(commit = True)
      # profile = Profile(user=user, phone = self.cleaned_data['phone'])
      # profile.save()
      # return user, profile
      return user

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