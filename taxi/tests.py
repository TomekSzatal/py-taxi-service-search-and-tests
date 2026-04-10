from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer, Driver, Car
from taxi.forms import CarForm, DriverCreationForm, DriverLicenseUpdateForm
from taxi.admin import DriverAdmin, CarAdmin


# -------------------------
# MODELS TESTS
# -------------------------
class ModelTests(TestCase):
    def test_manufacturer_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        self.assertEqual(str(manufacturer), "BMW Germany")

    def test_driver_str(self):
        driver = Driver.objects.create_user(
            username="john",
            password="12345",
            license_number="ABC12345",
            first_name="John",
            last_name="Doe",
        )
        self.assertIn("john", str(driver))

    def test_car_str(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        car = Car.objects.create(model="X5", manufacturer=manufacturer)
        self.assertEqual(str(car), "X5")


# -------------------------
# FORMS TESTS
# -------------------------
class DriverFormTests(TestCase):
    def test_valid_driver_creation(self):
        form = DriverCreationForm(data={
            "username": "john",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        })
        self.assertTrue(form.is_valid())

    def test_invalid_license(self):
        form = DriverCreationForm(data={
            "username": "john",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "bad",
            "first_name": "John",
            "last_name": "Doe",
        })
        self.assertFalse(form.is_valid())


class CarFormTests(TestCase):
    def test_car_form_valid(self):
        manufacturer = Manufacturer.objects.create(
            name="BMW",
            country="Germany",
        )
        driver = Driver.objects.create_user(
            username="john",
            password="12345",
            license_number="ABC12345",
        )

        form = CarForm(data={
            "model": "X5",
            "manufacturer": manufacturer.id,
            "drivers": [driver.id],
        })

        self.assertTrue(form.is_valid())


# -------------------------
# VIEWS TESTS
# -------------------------
class IndexViewTests(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="12345",
            license_number="ABC12345",
        )
        self.client.force_login(self.user)

    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Drivers")
        self.assertContains(response, "Cars")
        self.assertContains(response, "Manufacturers")


# -------------------------
# ADMIN TESTS (basic)
# -------------------------
class AdminTests(TestCase):
    def test_driver_admin_registered_fields(self):
        self.assertIn("license_number", DriverAdmin.list_display)

    def test_car_admin_search(self):
        self.assertIn("model", CarAdmin.search_fields)
