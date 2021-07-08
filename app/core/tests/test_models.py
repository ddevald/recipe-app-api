from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='dev@mustang.com', password='mustang123'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test create user with email successful"""
        email = 'dev@ownsmustang.com'
        password = 'mustang123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test normalizing the email address"""
        email = 'dev@OWNSMUSTANG.COM'
        user = get_user_model().objects.create_user(email, 'Mustang123')

        self.assertEqual(user.email, email.lower())

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

    def test_tag_str(self):
        """test tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)
