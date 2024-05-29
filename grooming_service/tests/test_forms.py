from django.test import TestCase
from grooming_service.forms import *
from grooming_service.models import *


class TestRegisterUserForm(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            first_name="John",
            last_name="Travolta",
            email="johntravolta@example.com",
            password="password123",
            phone_number="1234567890",
            address="somewhere over the rainbow"
        )

    def test_register_user_form_is_valid(self):
        form = RegistrationForm(data={
            'first_name': 'Johnny',
            'last_name': 'Bravo',
            'email': 'johnnybravo@example.com',
            'password': 'password123',
            'phone_number': '0987654321',
            'address': '456 Elm St'
        })
        self.assertTrue(form.is_valid())

    def test_duplicate_email(self):
        form = RegistrationForm(data={
            'first_name': 'John',
            'last_name': 'Travolta',
            'email': 'johntravolta@example.com',
            'password': 'password123',
            'phone_number': '4123144545',
            'address': '456 Elm St'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
        self.assertEqual(form.errors['email'], ["This email is already in use."])

    def test_invalid_email_format(self):
        form = RegistrationForm(data={
            'first_name': 'Johnny',
            'last_name': 'Bravo',
            'email': 'johnnybravo',
            'password': 'password123',
            'phone_number': '0987654321',
            'address': '456 Elm St'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_duplicate_phone_number(self):
        form = RegistrationForm(data={
            'first_name': 'John',
            'last_name': 'Travolta',
            'email': 'johntravolta234@example.com',
            'password': 'password123',
            'phone_number': '1234567890',
            'address': '456 Elm St'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertEqual(form.errors['phone_number'], ["This phone number is already in use."])

    def test_phone_number_with_letters(self):
        form = RegistrationForm(data={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'janesmith@example.com',
            'password': 'password123',
            'phone_number': '123ABC7890',
            'address': '456 Elm St'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)
        self.assertEqual(form.errors['phone_number'], ["Phone number can contain only digits."])

    def test_missing_fields(self):
        form = RegistrationForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('password', form.errors)
        self.assertIn('phone_number', form.errors)
        self.assertIn('address', form.errors)