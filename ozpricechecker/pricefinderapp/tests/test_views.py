"""Tet views."""

from django.contrib.auth.models import User
# from django.urls import reverse
from django.test import TestCase
from pricefinderapp.models import Currency, Store, Product, ProductPrice  # , UserProduct


class ProjectTests(TestCase):
    def test_homepage(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/userproduct/'))


class UserProductListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        # Setup run before every test method.
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_user_login_userproduct_view(self):
        self.assertTrue(self.user)

        logged_in = self.client.login(username='testuser', password='12345')
        self.assertTrue(logged_in)

        response = self.client.get('')
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/userproduct/')
        self.assertTemplateUsed(response, 'pricefinderapp/userproduct_list.html')
        self.assertContains(response, self.user, count=2, status_code=200)

    def test_post_method_user_login_userproduct_view(self):
        response = self.client.post('/accounts/login/', {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/userproduct/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pricefinderapp/userproduct_list.html')
        self.assertContains(response, self.user, count=2, status_code=200)

    def test_user_notlogin_userproduct_view(self):
        response = self.client.get('/userproduct/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))


class UserProductCreateViewTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.currency = Currency.objects.create(name='AUD')
        self.store = Store.objects.create(name='Woolworths', currency=self.currency)
        self.product = Product.objects.create(store=self.store, name='avocado organic')
        self.productprice = ProductPrice.objects.create(product=self.product, price='5')
        # self.userproduct = UserProduct.objects.create(product=self.product, user=self.user, threshhold=5.00)

    def test_add_userproduct_view(self):
        self.assertTrue(self.user)

        logged_in = self.client.login(username='testuser', password='12345')
        self.assertTrue(logged_in)

        # response = self.client.get('')
        # self.assertEqual(response.status_code, 302)

        # response = self.client.get('/adduserproduct/')
        # self.assertTemplateUsed(response, 'pricefinderapp/userproduct_add.html')
        # self.assertEqual(response.status_code, 200)

        response = self.client.post('/adduserproduct/', {
            'product': 'avocado organic',
            'user': 'testuser',
            'threshhold': 5.00
        })
        # response = self.client.post(reverse('userproduct_add'), {
        #     'product': self.product,
        #     'user': self.user,
        #     'threshhold': 5.00
        # })
        # print(response)
        # print(response.url)
        self.assertTemplateUsed(response, 'pricefinderapp/userproduct_add.html')
        # print(UserProduct.objects.all())
        # print(ProductPrice.objects.all())
        # print(Product.objects.all())
        # print(Store.objects.all())

        # self.assertEqual(UserProduct.objects.last().threshhold, 5.00)

    # def test_post_method_user_login_userproduct_view(self):
    #     response = self.client.post('/accounts/login/', {'username': 'testuser', 'password': '12345'})
    #     self.assertEqual(response.status_code, 302)
    #     response = self.client.get('/userproduct/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'pricefinderapp/userproduct_list.html')
    #     self.assertContains(response, self.user, count=2, status_code=200)

    # def test_user_notlogin_userproduct_view(self):
    #     response = self.client.get('/userproduct/')
    #     self.assertEqual(response.status_code, 302)
