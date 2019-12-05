from django.test import TestCase

from pricefinderapp.models import Currency, Product, Store


class SetupTests(TestCase):

    def setUp(self):
        currency = Currency.objects.create(name='AUD')
        self.store = Store.objects.create(name='Woolworths', currency=currency)

    def test_str_no_name(self):
        product = Product.objects.create(store=self.store, prod_url='/1234/Tomatoes')
        self.assertEqual(str(product), '')

    def test_str_name(self):
        product = Product.objects.create(store=self.store, prod_url='/1234/Tomatoes', name='Super Tomatoes')
        self.assertEqual(str(product), 'Super Tomatoes')
