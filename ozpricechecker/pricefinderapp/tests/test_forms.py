"""Testing forms."""

from unittest import mock

from django.test import TestCase

from pricefinderapp.forms import StoreCreateForm
from pricefinderapp.models import Currency

import ezscrape.scraping.scraper

def mocked_check_url_online(**kargs):
    return True

def mocked_check_url_offline(**kargs):
    return False

class TestStoreCreateForm(TestCase):
    def setUp(self):
        self.currency = Currency.objects.create(name='AUD')

    @mock.patch('ezscrape.scraping.scraper.check_url')
    def test_valid_form_created(self, mocked_db):
        #scraper.check_url = mock.MagicMock(name='mocked_check_url_online')
        ezscrape.scraping.scraper.check_url = mock.MagicMock(return_value=True)
        url = 'http://www.url.com'
        form_data = {
            'name': 'TestStore',
            'prod_base_url': url,
            'currency': self.currency,
            'dynamic_page': True,
        }

        form = StoreCreateForm(data=form_data)
        form.is_valid()
        #self.assertTrue(form.is_valid())

        self.assertEqual(form.cleaned_data['name'], 'TestStore')
        self.assertEqual(form.cleaned_data['prod_base_url'], url)
        self.assertEqual(form.cleaned_data['currency'], self.currency)
        self.assertEqual(form.cleaned_data['dynamic_page'], True)






    '''
    def test_form_creation(self):
        url = 'http://www.this-is-not-a-valid-url.comde'
        form_data = {
            'name': 'TestStore',
            'prod_base_url': url,
            'currency': self.currency,
            'dynamic_page': True,
        }

        form = StoreCreateForm(data=form_data)
        #self.assertFalse(form.is_valid())

        print(form)
        form.is_valid()
        print("\n### form['prod_base_url']", form['prod_base_url'])
        print('\n### cleaned', form.cleaned_data)
        #self.assertEqual(form['prod_base_url'], url)


        #print(form)
        #self.assertTrue(form.is_valid())
        #form.is_valid()
        print('cleaned', form.cleaned_data)
        self.assertEqual(form.clean_prod_base_url(), url)

        #self.assertFalse(True)
    '''



    ''' TODO

    def test_form_url_valid(self):
    def test_form_url_invalid_format(self):
    def test_form_url_not_online(self):


    '''

