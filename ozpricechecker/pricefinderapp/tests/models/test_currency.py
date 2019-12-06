from django.test import TestCase

from pricefinderapp.models import Currency


class SetupTests(TestCase):

    def test_str(self):
        currency = Currency.objects.create(name='AUD')
        self.assertEqual(str(currency), 'AUD')
