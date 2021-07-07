from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)

    class PublicUserApiTest(TestCase):
        """Test the users API (public)"""

        def setUp(self):
            self.client = APIClient()

        def test_Create_valid_user_success(self):
            """Test creating user with valid payload is successful"""
            payload = {
                'email': 'Dev@hasmustang.com',
                'password': 'Mustang111',
                'name': 'Dev Mustang'
            }
            res = self.client.post(CREATE_USER_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            user = get_user_model().objects.get(**res.data)
            self.assertTrue(user.check_password(payload['password']))
            self.assertNotIn('password', res.data)

        def test_user_exists(self):
            """Test creating a user that already exists that fails"""
            payload = {'email': 'Dev@mustang.com', 'password': 'Mustang111'}
            create_user(**payload)

            res = self.client.post(CREATE_USER_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_password_too_short(self):
            """The password must be more than 5 characters"""
            payload = {
                'email': 'Dev@mustang.com',
                'password': 'Mu',
                'name': 'Dev'}
            res = self.client.post(CREATE_USER_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_BAD_REQUEST)
            user_exists = get_user_model().objects.filter(
                email=payload['email']
            ).exists()
            self.assertFalse(user_exists)

        def test_create_token_for_user(self):
            """Test that a token is created for the user"""
            payload = {'email': 'test@mustang.com', 'password': 'password1'}
            create_user(**payload)
            res = self.client.post(TOKEN_URL, payload)

            self.assertIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTPS_200_OK)

        def test_token_invalid_credentials(self):
            """testing that token is not created if invalid credentials"""
            create_user(email='dev@gmail.com', password='mustang1')
            payload = {'email': 'dev@gmail.com', 'password': 'password'}
            res = self.client.post(TOKEN_URL, payload)

            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_no_user(self):
            """test that the token is created if the user does not exists"""
            payload = {'email': 'dev@gmail.com', 'password': 'mustang1'}
            res = self.client.post(TOKEN_URL, payload)

            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_missing_field(self):
            """testing that email and password are required"""
            res = self.client.post(TOKEN_URL, {
                                            'email': 'one',
                                            'password': 'two'
            })
            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
