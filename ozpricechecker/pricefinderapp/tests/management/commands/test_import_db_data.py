
from pathlib import Path

import os
import pytest

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from pricefinderapp.models import (
    Currency, Product, ScrapeType, ScrapeTemplate, Store
)

class CommandArgumentTestCase(TestCase):

    def test_no_argument_given(self):
        with pytest.raises(CommandError):
            args = []
            opts = {}
            call_command('import_db_data', *args, **opts)

    def test_invalid_directory_specified(self):
        invalid_path = 'this-is-not-a-path'
        self.assertFalse(os.path.exists(invalid_path))

        with pytest.raises(CommandError):
            args = [invalid_path]
            opts = {}
            call_command('import_db_data', *args, **opts)

    def test_csv_files_not_found(self):
        path = Path('ozpricechecker') / 'pricefinderapp' / 'tests'
        self.assertTrue(os.path.exists(path))

        with pytest.raises(CommandError):
            args = [path]
            opts = {}
            call_command('import_db_data', *args, **opts)


class CommandsTestCase(TestCase):

    def setUp(self):
        args = [Path('ozpricechecker') / 'pricefinderapp' / 'tests' / 'TestFiles' / 'DbData']
        opts = {}
        call_command('import_db_data', *args, **opts)

    def test_currency(self):
        currencies = Currency.objects.all()
        self.assertEqual(currencies.count(), 1)

        currency = currencies.first()
        self.assertEqual(currency.name, 'AUD')

    def test_store(self):
        stores = Store.objects.all()
        self.assertEqual(stores.count(), 1)

        store = stores.first()
        self.assertEqual(store.name, 'Woolworth')
        self.assertEqual(store.prod_base_url, 'https://www.woolworths.com.au/shop/productdetails')
        self.assertTrue(store.dynamic_page)
        self.assertEqual(store.currency, Currency.objects.get(name='AUD'))

    def test_scrape_type(self):
        scrape_types = ScrapeType.objects.all()
        self.assertEqual(scrape_types.count(), 1)

        scrape_type = scrape_types.first()
        self.assertEqual(scrape_type.name, 'Price')

    def test_scrape_template(self):
        scrape_templates = ScrapeTemplate.objects.all()
        self.assertEqual(scrape_templates.count(), 1)

        scrape_template = scrape_templates.first()
        self.assertEqual(scrape_template.store, Store.objects.get(name='Woolworth'))
        self.assertEqual(scrape_template.scrape_type, ScrapeType.objects.get(name='Price'))
        self.assertEqual(scrape_template.xpath, '//fake-xpath')

    def test_product(self):
        prods = Product.objects.all()
        self.assertEqual(prods.count(), 1)

        prod = prods.first()
        self.assertEqual(prod.store, Store.objects.get(name='Woolworth'))
        self.assertEqual(prod.prod_url, '601343/woolworths-jasmine-rice')
        self.assertEqual(prod.name, 'Woolworths Jasmine Rice 5kg')
