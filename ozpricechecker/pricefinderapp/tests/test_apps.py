from django.test import TestCase

from pricefinderapp.apps import PricefinderappConfig


class TestConfigName(TestCase):

    def test_name(self):
        self.assertEqual(PricefinderappConfig.name, 'pricefinderapp')
