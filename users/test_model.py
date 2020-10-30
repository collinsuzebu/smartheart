from django.test import TestCase
from django.contrib.auth import get_user_model

from django.db.utils import IntegrityError


password = "abcde123!!"
email = "testuser@gmail.com"
superuser_email = 'superuser@gmail.com'

class UsersManagersTests(TestCase):

	def test_create_user(self):
		User = get_user_model()
		user = User.objects.create_user(email=email, password=password)
		self.assertEqual(user.email, email)
		self.assertTrue(user.is_active)
		self.assertFalse(user.is_staff)
		self.assertFalse(user.is_superuser)

		try:
			# username is None for the AbstractUser option
			# username is does not exist for the AbstractBaseUser
			self.assertIsNone(user.username)
		except AttributeError:
			pass

		with self.assertRaises(TypeError):
			User.objects.create_user()

		with self.assertRaises(TypeError):
			User.objects.create_user(email="")

		with self.assertRaises(ValueError):
			User.objects.create_user(email="", password=password)

		with self.assertRaises(IntegrityError) as context:
			User.objects.create_user(email=email, password="abcfegh")
			self.assertTrue('UNIQUE constraint failed' in str(context.exception))


	def test_create_superuser(self):
		User = get_user_model()
		admin_user = User.objects.create_superuser(superuser_email, password)
		self.assertEqual(admin_user.email, superuser_email)
		self.assertTrue(admin_user.is_active)
		self.assertTrue(admin_user.is_staff)
		self.assertTrue(admin_user.is_superuser)

		try:
			# username is None for the AbstractUser option
			# username is does not exist for the AbstractBaseUser
			self.assertIsNone(admin_user.username)
		except AttributeError:
			pass

		with self.assertRaises(ValueError):
			User.objects.create_superuser(
				email=superuser_email, password=password, is_superuser=False)