from django.test import TestCase
from django.contrib.auth import get_user_model
from grooming_service.models import *
from datetime import datetime

User = get_user_model()


class TestUserModel(TestCase):
    def test_create_user(self):
        # Test creating a user with required fields
        user = User.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            address='123 Main St'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertEqual(user.address, '123 Main St')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        # Test creating a superuser with required fields
        superuser = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123'
        )
        self.assertEqual(superuser.email, 'admin@example.com')
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)


class TestServiceModel(TestCase):
    def setUp(self):
        self.service = Service.objects.create(
            name="Bathing",
            description="Bathing service description",
            vary_price1=20,
            vary_price2=30,
            image='images/bathing.jpg',
            short_description="Short description for bathing service"
        )

    def test_service_creation(self):
        self.assertEqual(self.service.name, "Bathing")
        self.assertEqual(self.service.description, "Bathing service description")
        self.assertEqual(self.service.vary_price1, 20)
        self.assertEqual(self.service.vary_price2, 30)
        self.assertEqual(self.service.image, 'images/bathing.jpg')
        self.assertEqual(self.service.short_description, "Short description for bathing service")

    def test_service_string_representation(self):
        self.assertEqual(str(self.service), "Bathing")

    def test_default_short_description(self):
        service_without_short_description = Service.objects.create(
            name="Grooming",
            description="Grooming service description",
            vary_price1=25,
            vary_price2=35,
            image='images/grooming.jpg'
        )
        self.assertEqual(service_without_short_description.short_description, "")


class TestPetModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user for testing
        cls.user = User.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            address='123 Main St'
        )

    def setUp(self):
        # Create a pet object for each test
        self.pet = Pet.objects.create(name='Buddy', breed='Labrador', age=3, user=self.user)

    def test_pet_creation(self):
        # Check if the pet object is created properly
        self.assertEqual(self.pet.name, 'Buddy')
        self.assertEqual(self.pet.breed, 'Labrador')
        self.assertEqual(self.pet.age, 3)
        self.assertEqual(self.pet.user, self.user)

    def test_str_representation(self):
        # Check if the __str__ method returns the name of the pet
        self.assertEqual(str(self.pet), 'Buddy')

    def test_default_image(self):
        # Check if the default image is set properly
        self.assertEqual(self.pet.image.name, 'media/images/tey9seavfcldmybatmmt')

    def test_medical_notes_nullable(self):
        # Check if medical_notes field is nullable
        self.pet.medical_notes = "Some medical notes"
        self.pet.save()
        self.assertEqual(self.pet.medical_notes, "Some medical notes")

    def test_db_table_name(self):
        # Check if the database table name is correct
        table_name = Pet._meta.db_table
        self.assertEqual(table_name, 'grooming_service_pet')



class TestAppointmentModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a user, service, and pet for testing
        cls.user =User.objects.create_user(
            email='test@example.com',
            password='password123',
            first_name='John',
            last_name='Doe',
            phone_number='1234567890',
            address='123 Main St'
        )
        cls.pet = Pet.objects.create(name='Buddy', breed='Labrador', age=3, user=cls.user)
        cls.service = Service.objects.create(name='Grooming', description='Pet grooming service')

    def setUp(self):
        # Create an appointment object for each test
        self.appointment = Appointment.objects.create(user=self.user, service=self.service, pet=self.pet,
                                                       status=STATUS[0][0], start_date_time=datetime.now())

    def test_appointment_creation(self):
        # Check if the appointment object is created properly
        self.assertEqual(self.appointment.user, self.user)
        self.assertEqual(self.appointment.service, self.service)
        self.assertEqual(self.appointment.pet, self.pet)
        self.assertEqual(self.appointment.status, STATUS[0][0])

    def test_str_representation(self):
        # Check if the __str__ method returns the name of the pet for appointment
        self.assertEqual(str(self.appointment), 'Buddy')

    def test_default_status(self):
        # Check if the default status is set properly
        self.assertEqual(self.appointment.status, STATUS[0][0])

    def test_db_table_name(self):
        # Check if the database table name is correct
        table_name = Appointment._meta.db_table
        self.assertEqual(table_name, 'grooming_service_appointment')


