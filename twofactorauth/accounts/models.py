from django.db import models
# from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# for baseuser
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, username,email, password, **extra_fields):
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self,username, email, password=None, **extra_fields):
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(username,email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(username,email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(_('username'),max_length=30, unique=True)
	password = models.CharField(max_length=30)
	phone = models.CharField(max_length=20,unique=True)
	email = models.EmailField(_('email address'), unique=True)
	first_name = models.CharField(_('first name'), max_length=30, blank=True)
	last_name = models.CharField(_('last name'), max_length=30, blank=True)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	is_active = models.BooleanField(_('active'), default=True)
	is_admin = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.first_name

	def __str__():
		self.username

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	@property
	def is_staff(self):
		"Is the user a member of staff?"
		# Simplest possible answer: All admins are staff
		return self.is_admin

	# def email_user(self, subject, message, from_email=None, **kwargs):
	# 	send_mail(subject, message, from_email, [self.email], **kwargs)




# class Profile(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	phone = models.CharField(max_length=20,unique=True)

# 	def __str__(self):
# 		return self.user.username

# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()