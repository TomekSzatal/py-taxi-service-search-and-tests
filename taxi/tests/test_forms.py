from django.test import TestCase
from taxi.forms import (
    CarForm,
    DriverCreationForm,
    DriverLicenseUpdateForm,
)
from taxi.models import Driver, Manufacturer, Car


class DriverFormTests(TestCase):
    def test_driver_creation_form_valid(self):
        form_data = {
            "username": "john",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "ABC12345",
            "first_name": "John",
            "last_name": "Doe",
        }

        form = DriverCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_driver_creation_form_invalid_license(self):
        form_data = {
            "username": "john",
            "password1": "StrongPass123",
            "password2": "StrongPass123",
            "license_number": "invalid",  # zła długość i format
            "first_name": "John",
            "last_name": "Doe",
        }

        form = DriverCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class DriverLicenseUpdateFormTests(TestCase):
    def test_valid_license(self):
        driver = Driver.objects.create_user(
            username="john",
            password="12345",
            license_number="ABC12345"
        )

        form = DriverLicenseUpdateForm(
            data={"license_number": "XYZ54321"},
            instance=driver
        )

        self.assertTrue(form.is_valid())

    def test_invalid_license_length(self):
        driver = Driver.objects.create_user(
            username="john",
            password="12345",
            license_number="ABC12345"
        )

        form = DriverLicenseUpdateForm(
            data={"license_number": "SHORT"},
            instance=driver
        )

        self.assertFalse(form.is_valid())

    def test_invalid_license_format(self):
        driver = Driver.objects.create_user(
            username="john",
            password="12345",
            license_number="ABC12345"
        )

        form = DriverLicenseUpdateForm(
            data={"license_number": "abc12345"},
            instance=driver
        )

        self.assertFalse(form.is_valid())


class CarFormTests(TestCase):
    def test_car_form_valid(self):
        manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

        driver = Driver.objects.create_user(
            username="john",
            password="12345",
            license_number="ABC12345"
        )

        form_data = {
            "model": "Model S",
            "manufacturer": manufacturer.id,
            "drivers": [driver.id],
        }

        form = CarForm(data=form_data)
        self.assertTrue(form.is_valid())
