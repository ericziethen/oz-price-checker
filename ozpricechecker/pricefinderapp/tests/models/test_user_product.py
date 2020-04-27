from django.test import TestCase

from pricefinderapp.models import Currency, Product, Store, ProductPrice, UserProduct, User


class SetupTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        currency = Currency.objects.create(name='AUD')
        self.store = Store.objects.create(name='Woolworths', currency=currency)
        self.product = Product.objects.create(store=self.store, prod_url='/1234/Tomatoes', name='Super Tomatoes')
        self.product_price = ProductPrice.objects.create(product=self.product, price=10)

    def test_threshhold(self):
        user_product = UserProduct.objects.create(product=self.product, user=self.user, threshhold=5)
        self.assertEqual(user_product.threshhold, 5)

    def test_is_threshhold_reached_false(self):
        user_product = UserProduct.objects.create(product=self.product, user=self.user, threshhold=5)
        self.assertEqual(user_product.is_threshhold_reached, False)

    def test_is_threshhold_reached_true(self):
        user_product = UserProduct.objects.create(product=self.product, user=self.user, threshhold=10)
        self.assertEqual(user_product.is_threshhold_reached, True)

    def test_is_threshhold_reached_no_price(self):
        product = Product.objects.create(store=self.store, prod_url='/1234/Mango', name='Alphanso Mango')
        user_product = UserProduct.objects.create(product=product, user=self.user, threshhold=50)
        self.assertEqual(user_product.is_threshhold_reached, False)
        self.assertEqual(user_product.product.latest_price, None)
