from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib import admin

from taxi.admin import DriverAdmin, CarAdmin
from taxi.models import Driver, Car, Manufacturer


class AdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_driver_admin(self):
        driver_admin = DriverAdmin(Driver, self.site)

        self.assertIn("license_number", driver_admin.list_display)

        fieldsets = dict(driver_admin.fieldsets)
        self.assertIn("Additional info", fieldsets)

    def test_car_admin(self):
        car_admin = CarAdmin(Car, self.site)

        self.assertEqual(car_admin.search_fields, ("model",))
        self.assertEqual(car_admin.list_filter, ("manufacturer",))

    def test_manufacturer_registered(self):
        self.assertIn(Manufacturer, admin.site._registry)
