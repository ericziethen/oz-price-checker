from django.test import TestCase

from pricefinderapp.models import Currency, Store


class SetupTests(TestCase):

    def setUp(self):
        self.currency = Currency.objects.create(name='AUD')

    def test_str(self):
        store = Store.objects.create(name='Woolworths', currency=self.currency)
        self.assertEqual(str(store), 'Woolworths')
