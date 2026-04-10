from django.test import TestCase
from django.urls import reverse

from taxi.models import Driver, Manufacturer, Car


class BaseTestCase(TestCase):
    def setUp(self):
        self.user = Driver.objects.create_user(
            username="testuser",
            password="12345",
            license_number="ABC12345"
        )
        self.client.login(username="testuser", password="12345")

        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )


class PublicAccessTests(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertNotEqual(response.status_code, 200)


class IndexViewTests(BaseTestCase):
    def test_index_view(self):
        response = self.client.get(reverse("taxi:index"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Drivers")
        self.assertContains(response, "Cars")
        self.assertContains(response, "Manufacturers")


class DriverViewTests(BaseTestCase):
    def test_driver_list(self):
        response = self.client.get(reverse("taxi:driver-list"))
        self.assertEqual(response.status_code, 200)

    def test_driver_search(self):
        Driver.objects.create_user(
            username="john_doe",
            password="12345",
            license_number="XYZ12345"
        )

        response = self.client.get(
            reverse("taxi:driver-list"),
            {"q": "john"}
        )

        self.assertContains(response, "john_doe")

    def test_driver_detail(self):
        response = self.client.get(
            reverse("taxi:driver-detail", args=[self.user.id])
        )
        self.assertEqual(response.status_code, 200)


class CarViewTests(BaseTestCase):
    def test_car_list(self):
        response = self.client.get(reverse("taxi:car-list"))
        self.assertEqual(response.status_code, 200)

    def test_car_search(self):
        Car.objects.create(
            model="Corolla",
            manufacturer=self.manufacturer
        )

        response = self.client.get(
            reverse("taxi:car-list"),
            {"q": "Model"}
        )

        self.assertContains(response, "Model S")
        self.assertNotContains(response, "Corolla")

    def test_car_detail(self):
        response = self.client.get(
            reverse("taxi:car-detail", args=[self.car.id])
        )
        self.assertEqual(response.status_code, 200)


class ManufacturerViewTests(BaseTestCase):
    def test_manufacturer_list(self):
        response = self.client.get(reverse("taxi:manufacturer-list"))
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_search(self):
        Manufacturer.objects.create(name="Toyota", country="Japan")

        response = self.client.get(
            reverse("taxi:manufacturer-list"),
            {"q": "Tes"}
        )

        self.assertContains(response, "Tesla")
        self.assertNotContains(response, "Toyota")


class ToggleAssignTests(BaseTestCase):
    def test_assign_driver_to_car(self):
        response = self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )

        self.assertRedirects(
            response,
            reverse("taxi:car-detail", args=[self.car.id])
        )

        self.assertIn(self.user, self.car.drivers.all())

    def test_remove_driver_from_car(self):
        self.car.drivers.add(self.user)

        self.client.get(
            reverse("taxi:toggle-car-assign", args=[self.car.id])
        )

        self.assertNotIn(self.user, self.car.drivers.all())
