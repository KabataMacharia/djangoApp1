from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Profile
from django.core import validators
from django.core.exceptions import ValidationError

# for ensuring the phone number is unique
def validate_phone(value):
  if Profile.objects.filter(phone=value).exists():
    raise ValidationError("This phone number:"+value+" is already used ")

class SignUpForm(UserCreationForm):
    phone = forms.CharField(help_text='Your phone number',validators=[validate_phone])

    class Meta:
        model = User
        fields = ('username', 'phone', 'password1', 'password2', )
    def save(self, commit=True):
      if not commit:
        raise NotImplementedError("Can't create User and UserProfile without database save")
      user = super().save(commit = True)
      profile = Profile(user=user, phone = self.cleaned_data['phone'])
      profile.save()
      return user, profile

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