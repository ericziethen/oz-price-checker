"""Tet views."""

from django.contrib.auth.models import User
from django.test import TestCase


class ProjectTests(TestCase):
    def test_homepage(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 302)


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
