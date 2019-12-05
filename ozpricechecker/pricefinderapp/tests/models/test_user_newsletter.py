from django.contrib.auth.models import User
from django.test import TestCase

from pricefinderapp.models import UserNewsLetter


class SetupTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_str_no_name(self):
        newsletter = UserNewsLetter(user=self.user)
        self.assertEqual(str(newsletter), '')

    def test_str_name(self):
        newsletter = UserNewsLetter(user=self.user, name='My first Newsletter')
        self.assertEqual(str(newsletter), 'My first Newsletter')
