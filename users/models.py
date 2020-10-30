import datetime

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken

from .managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(_('email address'), unique=True, db_index=True)
	first_name = models.CharField(blank=True, max_length=30, verbose_name='first name')
	last_name = models.CharField(blank=True, max_length=30, verbose_name='last name')
	is_staff = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(default=timezone.now)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = CustomUserManager()


	def __str__(self):
		return self.email


	def token(self):
		refresh = RefreshToken.for_user(self)

		return {
			'refresh': str(refresh),
			'access': str(refresh.access_token)
		}







	# @property
	# def token(self):
	# 	return self.generate_access_token()


	# 	# refresh = RefreshToken.for_user(self)

	# 	# return {
	# 	# 	'refresh': str(refresh),
	# 	# 	'access': str(refresh.access_token)
	# 	# }


	# def generate_access_token(self):

	#     access_token_payload = {
	#         'id': self.pk,
	#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=5),
	#         'iat': datetime.datetime.utcnow(),
	#     }
	#     access_token = jwt.encode(access_token_payload,
	#                               settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
	#     return access_token