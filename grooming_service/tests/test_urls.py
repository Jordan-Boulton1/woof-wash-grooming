from django.test import TestCase
from django.urls import reverse, resolve
from grooming_service import views


class TestUrls(TestCase):
    def test_register_url_resolves(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, views.register)

    def test_home_url_resolves(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)

    def test_about_url_resolves(self):
        url = reverse('about')
        self.assertEqual(resolve(url).func, views.about)

    def test_services_url_resolves(self):
        url = reverse('services')
        self.assertEqual(resolve(url).func, views.get_services)

    def test_login_url_resolves(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func, views.user_login)

    def test_logout_url_resolves(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func, views.user_logout)

    def test_appointment_url_resolves(self):
        url = reverse('appointment')
        self.assertEqual(resolve(url).func, views.book_appointment)

    def test_profile_url_resolves(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, views.manage_profile)

    def test_edit_profile_url_resolves(self):
        url = reverse('edit_profile')
        self.assertEqual(resolve(url).func, views.edit_profile)

    def test_get_appointment_by_id_url_resolves(self):
        url = reverse('get_appointment_by_id', args=[1])  # Change 1 to any valid appointment_id
        self.assertEqual(resolve(url).func, views.get_appointment_by_id)

    def test_cancel_appointment_url_resolves(self):
        url = reverse('cancel_appointment', args=[1])  # Change 1 to any valid cancel_appointment_id
        self.assertEqual(resolve(url).func, views.cancel_appointment)

    def test_delete_pet_url_resolves(self):
        url = reverse('delete_pet', args=[1])  # Change 1 to any valid delete_pet_id
        self.assertEqual(resolve(url).func, views.delete_pet)

    def test_get_pet_by_id_url_resolves(self):
        url = reverse('get_pet_by_id', args=[1])  # Change 1 to any valid pet_id
        self.assertEqual(resolve(url).func, views.get_pet_by_id)

    def test_delete_user_url_resolves(self):
        url = reverse('delete_user', args=[1])  # Change 1 to any valid delete_user_id
        self.assertEqual(resolve(url).func, views.delete_user)

    def test_service_price_url_resolves(self):
        url = reverse('service_price', args=[1])  # Change 1 to any valid service_id
        self.assertEqual(resolve(url).func, views.get_service_price)

    def test_not_found_url_resolves(self):
        url = reverse('not_found')
        self.assertEqual(resolve(url).func, views.not_found)
