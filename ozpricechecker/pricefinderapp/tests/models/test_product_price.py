
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

from pricefinderapp.models import Currency, Product, Store, ProductPrice


class SetupTests(TestCase):

    def setUp(self):
        currency = Currency.objects.create(name='AUD')
        store = Store.objects.create(name='Woolworths', currency=currency)
        self.product = Product.objects.create(store=store, prod_url='/1234/Tomatoes')

    def test_create_object_all_args(self):
        time_now = timezone.now()
        prod_price = ProductPrice.objects.create(
            product=self.product, price=10, date_time=time_now)

        self.assertEqual(prod_price.product, self.product)
        self.assertEqual(prod_price.date_time, time_now)
        self.assertEqual(prod_price.price, 10)

    def test_create_not_date_time_specified(self):
        time_start = timezone.now()
        prod_price = ProductPrice.objects.create(
            product=self.product, price=10)
        time_end = timezone.now()

        self.assertTrue(time_start <= prod_price.date_time <= time_end)

    def test_create_no_price_given(self):
        with self.assertRaises(IntegrityError):
            ProductPrice.objects.create(product=self.product)
