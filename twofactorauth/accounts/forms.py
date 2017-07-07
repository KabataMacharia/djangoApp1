
from django import forms
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField, ReadOnlyPasswordHashWidget, UserCreationForm,
    PasswordResetForm as OldPasswordResetForm,
    UserChangeForm as DjangoUserChangeForm,
    AuthenticationForm as DjangoAuthenticationForm,
)
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import identify_hasher, UNUSABLE_PASSWORD_PREFIX
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.html import format_html

# for signup form
from django.core import validators
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as password_validate
from django.core import exceptions
# from .models import User

User = get_user_model()

class SignUpForm(forms.ModelForm):
    TYPES = (('SUPER','superuser'),('STAFF','staff'),('ADMIN','admin'), ) 
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(help_text='Enter a password matching the first one',widget=forms.PasswordInput)
    username = forms.CharField(widget=forms.TextInput)
    email = forms.CharField(help_text='A valid email address is required',max_length=100,widget=forms.EmailInput)
    is_staff =  forms.NullBooleanField()
    is_admin =  forms.NullBooleanField()
    is_superuser =  forms.NullBooleanField()
    # your_role = forms.ChoiceField(choices=TYPES )
        
    class Meta:
        model = User 
        fields = ('username','email', 'phone', 'password1', 'password2',  )
        
    def clean_password(self):
        # Check that the two password entries match
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")
        password_match = False
        errors=dict()
        
        if password1 == password2:
            password_match = True            
            #Passwords match, so validate password 
            try:
                password_validate.validate_password(password=password2)
                return password2
            except exceptions.ValidationError as e:
                errors['password2'] = list(e.messages)
                return errors             
        else:            
            password_match = False
            errors['password2'] = "Passwords don't match"
            return errors
        
            
        
    def clean_email(self):
        email = self.data.get("email")
        errors=dict()
        valid_email = False
        
        try:
            validators.validate_email(email)
            valid_email = True                            
        except:
            valid_email = False
            errors['email'] = "Enter a valid email address please" 
            return errors
        if valid_email:
            return email
            
    # def clean_username(self):
    #     username = self.data.get("username")
    #     errors=dict()
    #     valid_username = False
    #     try:
    #         validators.validate_slug(username)
    #         valid_username = True
    #     except:
    #         errors['username'] = "Username is not valid. Special characters used" 
    #         return errors
    #     if valid_username:
    #         if(User.objects.filter(username=username).exists()):
    #             errors['username'] = "Sorry, that Username exists" 
    #             return errors
    #         else:
    #             return username
    
    def clean_phone(self):
        phone = self.data.get("phone")
        errors=dict()
        valid_phone = False
        try:
            validators.validate_integer(phone)
            valid_phone_number = True
        except:
            # raise forms.ValidationError("Not a valid phone number. 0-9 only")
            # valid_phone_number = False
            errors['phone'] = "Not a valid phone number. 0-9 only" 
            return errors
        if valid_phone_number:
            return phone

# for ensuring the phone number is unique
def validate_phone(value):
  if User.objects.filter(phone=value).exists():
    raise ValidationError("This phone number:"+value+" is already used ")

# class SignUpForm(UserCreationForm):
#     # phone = forms.CharField(help_text='Your phone number',validators=[validate_phone,RegexValidator('^[0-9]{10}$', message="phone number should be 10 digits")])
#     phone = forms.CharField(help_text='Your phone number',validators=[RegexValidator('^[0-9]{10}$', message="phone number should be 10 digits")])

#     class Meta:
#         model = User
#         fields = ('username','email', 'phone', 'password1', 'password2', )
#     def save(self, commit=True):
#       if not commit:
#         raise NotImplementedError("Can't create User and UserProfile without database save")
#       user = super().save(commit = True)
#       # profile = Profile(user=user, phone = self.data['phone'])
#       # profile.save()
#       # return user, profile
#       return user

# for signin
class SignInForm(DjangoAuthenticationForm):
    code = forms.CharField()
    class Meta:
        model = User
        fields = ('username', 'password', )