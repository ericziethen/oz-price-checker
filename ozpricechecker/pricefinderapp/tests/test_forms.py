"""Testing forms."""

from django.test import TestCase

from pricefinderapp.forms import StoreCreateForm
from pricefinderapp.models import Currency


class TestStoreCreateForm(TestCase):
    def setUp(self):
        self.currency = Currency.objects.create(name='AUD')

    def test_valid_form_created(self):
        url = 'http://www.url.com'
        form_data = {
            'name': 'TestStore',
            'prod_base_url': url,
            'currency': self.currency,
            'dynamic_page': True,
        }

        form = StoreCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data['name'], 'TestStore')
        self.assertEqual(form.cleaned_data['prod_base_url'], url)
        self.assertEqual(form.cleaned_data['currency'], self.currency)
        self.assertEqual(form.cleaned_data['dynamic_page'], True)

    def test_form_created_url_invalid_schema(self):
        url = 'www.url.com'
        form_data = {
            'name': 'TestStore',
            'prod_base_url': url,
            'currency': self.currency,
            'dynamic_page': True,
        }

        form = StoreCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue(form.has_error('prod_base_url', code='invalid_format'))
