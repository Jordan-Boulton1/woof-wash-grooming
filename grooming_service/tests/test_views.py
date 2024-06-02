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
