
from django.test import TestCase
from django.utils import timezone

from parameterized import parameterized

from pricefinderapp.models import Currency, Product, Store, ProductPrice


class SetupTests(TestCase):

    def setUp(self):
        currency = Currency.objects.create(name='AUD')
        self.store = Store.objects.create(name='Woolworths', currency=currency)

    def test_str_no_name(self):
        product = Product.objects.create(store=self.store, prod_url='/1234/Tomatoes')
        self.assertEqual(str(product), 'Woolworths - ')

    def test_str_name(self):
        product = Product.objects.create(store=self.store, prod_url='/1234/Tomatoes', name='Super Tomatoes')
        self.assertEqual(str(product), 'Woolworths - Super Tomatoes')

    def test_latest_prod_price_date(self):
        product = Product.objects.create(store=self.store, prod_url='/1234/Tomatoes', name='Super Tomatoes')
        self.assertEqual(product.latest_price, None)
        self.assertEqual(product.date_for_latest_price, None)

        time_now = timezone.now()
        # Only Product = Latest Price
        product_price_1 = ProductPrice.objects.create(
            product=product, price=10, date_time=time_now)
        self.assertEqual(product.latest_price, product_price_1.price)
        self.assertEqual(product.date_for_latest_price, product_price_1.date_time)

        # 2nd Product, later time becomes latest Price
        product_price_2 = ProductPrice.objects.create(
            product=product, price=50, date_time=time_now + timezone.timedelta(seconds=10))
        self.assertEqual(product.latest_price, product_price_2.price)
        self.assertEqual(product.date_for_latest_price, product_price_2.date_time)

        # 3rd Product, Earlier time than 2nd, 2nd stays latest product
        product_price_3 = ProductPrice.objects.create(
            product=product, price=25, date_time=time_now + timezone.timedelta(seconds=5))
        self.assertEqual(product.latest_price, product_price_2.price)
        self.assertEqual(product.date_for_latest_price, product_price_2.date_time)

        # Delete 2nd, 3rd becomes Latest Price
        product_price_2.delete()
        self.assertEqual(product.latest_price, product_price_3.price)
        self.assertEqual(product.date_for_latest_price, product_price_3.date_time)


class TestProductAttributes(TestCase):

    def setUp(self):
        self.currency = Currency.objects.create(name='AUD')

    @parameterized.expand([
        ('', '/1234/Tomatoes', '/1234/Tomatoes'),
        ('', '1234/Tomatoes', '/1234/Tomatoes'),
        ('http://www.woolies.com.au', '/1234/Tomatoes', 'http://www.woolies.com.au/1234/Tomatoes'),
        ('http://www.woolies.com.au', '1234/Tomatoes', 'http://www.woolies.com.au/1234/Tomatoes'),
        ('http://www.woolies.com.au/', '/1234/Tomatoes', 'http://www.woolies.com.au/1234/Tomatoes'),
        ('http://www.woolies.com.au/', '1234/Tomatoes', 'http://www.woolies.com.au/1234/Tomatoes'),
        ('https://www.woolworths.com.au/shop/productdetails', 'prud_url_1',
         'https://www.woolworths.com.au/shop/productdetails/prud_url_1')
    ])
    def test_url_combines(self, store_url, prod_url, combined_url):
        store = Store.objects.create(name='Woolworths', currency=self.currency,
                                     prod_base_url=store_url)
        product = Product.objects.create(store=store, prod_url=prod_url,
                                         name='Super Tomatoes')

        self.assertEqual(product.full_url, combined_url)
