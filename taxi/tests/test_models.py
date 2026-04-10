from django.test import TestCase
from taxi.models import Manufacturer, Driver, Car


class ManufacturerModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )

    def test_str(self):
        self.assertEqual(str(self.manufacturer), "Tesla USA")

    def test_ordering(self):
        Manufacturer.objects.create(name="BMW", country="Germany")
        Manufacturer.objects.create(name="Audi", country="Germany")

        manufacturers = Manufacturer.objects.all()
        expected = sorted(manufacturers, key=lambda x: x.name)

        self.assertEqual(list(manufacturers), expected)


class DriverModelTest(TestCase):
    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="john",
            password="12345",
            first_name="John",
            last_name="Doe",
            license_number="ABC12345"
        )

    def test_str(self):
        self.assertEqual(str(self.driver), "john (John Doe)")

    def test_get_absolute_url(self):
        url = self.driver.get_absolute_url()
        self.assertIn(str(self.driver.id), url)


class CarModelTest(TestCase):
    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(
            name="Tesla",
            country="USA"
        )
        self.driver = Driver.objects.create_user(
            username="john",
            password="12345",
            license_number="ABC12345"
        )
        self.car = Car.objects.create(
            model="Model S",
            manufacturer=self.manufacturer
        )

    def test_str(self):
        self.assertEqual(str(self.car), "Model S")

    def test_relationship_with_driver(self):
        self.car.drivers.add(self.driver)

        self.assertIn(self.driver, self.car.drivers.all())
        self.assertIn(self.car, self.driver.cars.all())
