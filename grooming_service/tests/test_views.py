from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from datetime import datetime
from django.utils import timezone

from grooming_service.forms import *


class TestNotFoundView(TestCase):
    def test_not_found_view(self):
        # Use the test client to make a GET request to the 'not_found' view
        response = self.client.get(reverse('not_found'))

        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the correct template was used
        self.assertTemplateUsed(response, '404.html')


class TestHomeView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up test data for the whole TestCase
        # Create 3 service instances, 2 with short descriptions and 1 without
        Service.objects.create(name="Service 1", short_description="Description 1")
        Service.objects.create(name="Service 2", short_description="Description 2")
        Service.objects.create(name="Service 3", short_description="")  # This should be excluded

    def test_home_view_status_code(self):
        # Use the test client to make a GET request to the 'home' view
        response = self.client.get(reverse('home'))
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        # Use the test client to make a GET request to the 'home' view
        response = self.client.get(reverse('home'))
        response = self.client.get(reverse('home'))
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/home.html')

    def test_home_view_context_data(self):
        # Use the test client to make a GET request to the 'home' view
        response = self.client.get(reverse('home'))
        # Check that 'home_services' is in the context
        self.assertIn('home_services', response.context)
        # Get the home services from the context
        home_services = response.context['home_services']
        # Check that there are 2 services in the context (the one without a short description is excluded)
        self.assertEqual(home_services.count(), 2)
        # Check that the services are ordered by '-id'
        self.assertEqual(home_services[0].name, "Service 2")
        self.assertEqual(home_services[1].name, "Service 1")


class TestAboutView(TestCase):
    def test_about_view_status_code(self):
        # Use the test client to make a GET request to the 'about' view
        response = self.client.get(reverse('about'))
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_about_view_template(self):
        # Use the test client to make a GET request to the 'about' view
        response = self.client.get(reverse('about'))
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/about.html')


class TestGetServicesView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up test data for the whole TestCase
        Service.objects.create(name="Service 1", short_description="Description 1")
        Service.objects.create(name="Service 2", short_description="Description 2")

    def test_get_services_view_status_code(self):
        # Use the test client to make a GET request to the 'get_services' view
        response = self.client.get(reverse('services'))
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_get_services_view_template(self):
        # Use the test client to make a GET request to the 'get_services' view
        response = self.client.get(reverse('services'))
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/services.html')

    def test_get_services_view_context_data(self):
        # Use the test client to make a GET request to the 'get_services' view
        response = self.client.get(reverse('services'))
        # Check that 'services' is in the context
        self.assertIn('services', response.context)
        # Get the services from the context
        services = response.context['services']
        # Check that there are 2 services in the context
        self.assertEqual(services.count(), 2)
        # Check the names of the services
        self.assertEqual(services[0].name, "Service 1")
        self.assertEqual(services[1].name, "Service 2")


class TestRegisterView(TestCase):
    def test_register_view_get_request(self):
        # Use the test client to make a GET request to the 'register' view
        response = self.client.get(reverse('register'))
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/register.html')
        # Check that the form is included in the context
        self.assertIsInstance(response.context['form'], RegistrationForm)

    def test_register_view_post_request_valid_form(self):
        # Use the test client to make a POST request to the 'register' view with valid data
        response = self.client.post(reverse('register'), {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'password123',
            'phone_number': '0987654321',
            'address': '456 Elm St'
        })
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 200)
        # Check that the user was created
        self.assertTrue(User.objects.filter(email='jane.smith@example.com').exists())
        # Check that the user is logged in
        user = User.objects.get(email='jane.smith@example.com')
        self.assertTrue(user.is_authenticated)
        # Check that the success message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(
            any(message.message == "Your account has been created! Logging you in..." for message in messages))

    def test_register_view_post_request_invalid_form(self):
        # Use the test client to make a POST request to the 'register' view with invalid data
        response = self.client.post(reverse('register'), {
            'first_name': '',
            'last_name': '',
            'email': 'invalidemail',
            'password': '',
            'phone_number': '',
            'address': ''
        })
        # Check that the response is 200 OK (form re-rendered with errors)
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/register.html')
        # Check that the form is included in the context and is not valid
        form = response.context['form']
        self.assertIsInstance(form, RegistrationForm)
        self.assertFalse(form.is_valid())
        # Check that the error messages were added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == "alert alert-danger" for message in messages))
        self.assertTrue(any(message.extra_tags == "register_form" for message in messages))


class TestUserLoginView(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up a test user for authentication
        User.objects.create_user(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            password='password123',
            phone_number='1234567890',
            address='123 Main St')

    def test_user_login_view_get_request(self):
        # Use the test client to make a GET request to the 'user_login' view
        response = self.client.get(reverse('login'))
        # Check that the response is 200 OK
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/login.html')
        # Check that the form is included in the context
        self.assertIsInstance(response.context['form'], LoginForm)

    def test_user_login_view_post_request_valid_credentials(self):
        # Use the test client to make a POST request to the 'user_login' view with valid credentials
        response = self.client.post(reverse('login'), {
            'email': 'john.doe@example.com',
            'password': 'password123'
        })
        # Check that the response is a redirect
        self.assertEqual(response.status_code, 200)
        # Check that the user is logged in
        user = User.objects.get(email='john.doe@example.com')
        self.assertTrue(user.is_authenticated)
        # Check that the success message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.message == "Login successful. Please wait..." for message in messages))

    def test_user_login_view_post_request_invalid_credentials(self):
        # Use the test client to make a POST request to the 'user_login' view with invalid credentials
        response = self.client.post(reverse('login'), {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        # Check that the response is 200 OK (form re-rendered with errors)
        self.assertEqual(response.status_code, 200)
        # Check that the correct template was used
        self.assertTemplateUsed(response, 'grooming_service/login.html')
        # Check that the form is included in the context and is not valid
        form = response.context['form']
        self.assertIsInstance(form, LoginForm)
        # Check that the error message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(message.level_tag == "alert alert-danger" for message in messages))
        self.assertTrue(any(message.extra_tags == "login_form" for message in messages))
