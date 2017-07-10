# for baseuser
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, phone, is_superuser, is_staff, is_admin, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, phone=phone, is_superuser=is_superuser, is_staff=is_staff,
                          is_admin=is_admin, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, phone, is_superuser, is_staff, is_admin, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        # extra_fields = {}
        return self._create_user(username, email, password, phone, is_superuser, is_staff, is_admin, **extra_fields)

    def create_superuser(self, username, email, password, phone, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, phone, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=120, unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True



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
