from django.test import TestCase

from pricefinderapp.models import Currency, ScrapeTemplate, ScrapeType, Store


class SetupTests(TestCase):

    def setUp(self):
        currency = Currency.objects.create(name='AUD')
        self.store = Store.objects.create(name='Woolworths', currency=currency)
        self.scrape_type = ScrapeType.objects.create(name='price')

    def test_str_no_xpath(self):
        template = ScrapeTemplate(store=self.store, scrape_type=self.scrape_type)
        self.assertEqual(str(template), '')

    def test_str_xpath(self):
        template = ScrapeTemplate(store=self.store, scrape_type=self.scrape_type, xpath='my_xpath')
        self.assertEqual(str(template), 'my_xpath')
