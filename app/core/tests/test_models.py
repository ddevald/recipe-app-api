from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test create user with email successful"""
        email = 'dev@ownsmustang.com'
        password = 'mustang123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEquals(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test normalizing the email address"""
        email = 'dev@OWNSMUSTANG.COM'
        user = get_user_model().objects.create_user(email, 'Mustang123')

        self.assertEquals(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raise value error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Mustang123')

    def test_create_new_superuser(self):
        """test creating a super user"""
        user = get_user_model().objects.create_superuser(
            'Dev@hasMustang.com',
            'Mustang123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
