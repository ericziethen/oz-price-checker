"""Tet views."""

from django.contrib.auth.models import User
from django.urls import  reverse_lazy #, resolve, reverse
from django.urls import reverse
from django.test import TestCase
# from pricefinderapp.views import UserProductListView

# class YourTestClass(TestCase):
#    @classmethod
#    def setUpTestData(cls):
#        # Run once to set up non-modified data for all class methods.
#        pass

#     def setUp(self):
#         # Setup run before every test method.
#         pass

#     def tearDown(self):
#         # Clean up run after every test method.
#         pass

#     def test_something_that_will_pass(self):
#         self.assertFalse(False)

#     def test_something_that_will_fail(self):
#         self.assertTrue(False)


class UserProductListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        # Setup run before every test method.
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_homepage(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 302)

    def test_user_login_userproduct_view(self):
        self.assertTrue(self.user)

        logged_in = self.client.login(username='testuser', password='12345')
        self.assertTrue(logged_in)

        response = self.client.get('')
        self.assertEqual(response.status_code, 302)
        # <HttpResponseRedirect status_code=302, "text/html; charset=utf-8", url="/userproduct/">

        response = self.client.get('/userproduct/')
        self.assertEqual(response.status_code, 200)
        # <TemplateResponse status_code=200, "text/html; charset=utf-8">

    def test_post_method_user_login_userproduct_view(self):
        response = self.client.post('/accounts/login/', {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 302)
        # <HttpResponseRedirect status_code=302, "text/html; charset=utf-8", url="/">

        response = self.client.get('/userproduct/')
        self.assertEqual(response.status_code, 200)
        # <TemplateResponse status_code=200, "text/html; charset=utf-8">

    def test_user_notlogin_userproduct_view(self):
        response = self.client.get('/userproduct/')
        self.assertEqual(response.status_code, 302)
        # When user not logged in then userproduct url rediret to login page
        # <HttpResponseRedirect status_code=302, "text/html; charset=utf-8", url="/accounts/login/?next=/userproduct/">
        # print(response)
        # print(response.content)
