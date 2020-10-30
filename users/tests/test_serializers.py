import json

from django.urls import reverse
from django.contrib.auth import get_user_model
from users.api.serializers import UserRegistrationSerializer, UserLoginSerializer
from django.db.utils import IntegrityError

from rest_framework.test import APITestCase




class UserRegistrationAPIViewTestCase(APITestCase):
    url = reverse("users:sign-up")

    def test_invalid_password(self):
        """
        Test to verify that a post call with invalid passwords
        """
        user_data = {
            "email": "test@testuser.com",
            "first_name": "testuserfirst",
            "last_name": "testuserlast",
            "password": "password",
            "confirm_password": "INVALID_PASSWORD"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_user_registration(self):
        """
        Test to verify that a post call with user valid data
        """
        user_data = {
            "email": "test@testuser.com",
            "first_name": "testuserfirst",
            "last_name": "testuserlast",
            "password": "123123abc!",
            "confirm_password": "123123abc!"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)
        # self.assertTrue("token" in json.loads(response.content))

    def test_unique_email_validation(self):
        """
        Test to verify that a post call with already exists email
        """
        user_data_1 = {
            "email": "test@testuser.com",
            "first_name": "testuserfirst",
            "last_name": "testuserlast",
            "password": "123123abc!",
            "confirm_password": "123123abc!"
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            "email": "test@testuser.com",
            "first_name": "first",
            "last_name": "last",
            "password": "xxdd23abc!",
            "confirm_password": "xxdd23abc!"
        }

        # response = self.client.post(self.url, user_data_2)
        # self.assertEqual(400, response.status_code)




class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("users:login")

    def setUp(self):
        self.email = "test@user.com"
        self.password = "123123abc_!"
        self.user = get_user_model().objects.create_user(self.email, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"email": self.email})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {"email": self.email, "password": "wrong_password"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"email": self.email, "password": self.password})
        self.assertEqual(200, response.status_code)
        # self.assertTrue("auth_token" in json.loads(response.content))



# class UserSerializerTests(TestCase):

# 	def setUp(self):
# 		self.user_attributes = {
# 			'email': 'useremail@user.com',
# 			'first_name': 'Tom',
# 			'last_name': 'Lop',
# 			'password': 'zoom2!opst'
# 		}

# 		self.serializer_data = {
# 			'email': 'secondemail@user.com',
# 			'first_name': 'Hans',
# 			'last_name': 'Mike',
# 			'password': 'jitoo2!mopst'
# 		}

# 		self.user = get_user_model().objects.create(**self.user_attributes)
# 		self.serializer = UserSerializer(instance=self.user)
		
# 	def test_contains_expected_fields(self):
# 		data = self.serializer.data

# 		self.assertCountEqual(data.keys(), ['email', 'first_name', 'last_name']) # password is read_only field

# 	def test_fields(self):
# 		data = self.serializer.data

# 		self.assertEqual(data['email'], self.user_attributes['email'])
# 		self.assertEqual(data['first_name'], self.user_attributes['first_name'])
# 		self.assertEqual(data['last_name'], self.user_attributes['last_name'])

# 	def test_invalid_email(self):
# 		self.serializer_data['email'] = ""

# 		serializer = UserSerializer(data=self.serializer_data)

# 		self.assertFalse(serializer.is_valid())
# 		self.assertCountEqual(serializer.errors, ['email'])


# 	def test_name_length_is_greater_than_one(self):
# 		self.serializer_data['first_name'] = "A"

# 		serializer = UserSerializer(data=self.serializer_data)
# 		self.assertFalse(serializer.is_valid())
# 		self.assertCountEqual(serializer.errors, ['first_name'])
# 		