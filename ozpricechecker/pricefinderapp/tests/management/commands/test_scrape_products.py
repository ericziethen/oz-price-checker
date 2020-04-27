from decimal import Decimal

import pytest

from django.test import TestCase

from pricefinderapp.models import (
    Currency, Product, ProductPrice, ScrapeTemplate, ScrapeType, Store
)
from pricefinderapp.management.commands import scrape_products
from tests import common


def test_no_xpath_values_specified():
    with pytest.raises(ValueError):
        scrape_products.process_url(common.TEST_PAGE_NOT_FOUND, {})


def test_invalid_url():
    xpath_dic = {
        'price': common.TEST_PAGE_WITH_PRICE_20_XPATH,
        'price-not-found': '//price-not-found/text()',
        'invalid_xpath': common.INVALID_XPATH
    }
    result = scrape_products.process_url(common.TEST_PAGE_NOT_FOUND, xpath_dic)

    assert 'values' not in result
    assert result['error']


def test_price_from_url():
    xpath_dic = {
        'price': common.TEST_PAGE_WITH_PRICE_20_XPATH,
        'price-not-found': '//price-not-found/text()',
        'invalid_xpath': common.INVALID_XPATH
    }
    result = scrape_products.process_url(common.TEST_PAGE_WITH_PRICE_20, xpath_dic)

    print('RESULT', result)

    assert result['values']['price']['value'] == '20'
    assert 'error' not in result['values']['price']

    assert result['values']['price-not-found']['value'] is None
    assert 'error' not in result['values']['price']

    assert 'value' not in result['values']['invalid_xpath']
    assert result['values']['invalid_xpath']['error']


VALID_DECIMAL_PRICES = [
    ('0', '0.00'),
    ('0.0', '0.00'),
    ('0.1', '0.10'),
    ('1', '1.00'),
    ('1.0', '1.00'),
    ('15.23', '15.23'),
    ('15.234', '15.23'),
    ('15.235', '15.24'),
    ('15.236', '15.24'),
]
@pytest.mark.parametrize('str_val, expected_val', VALID_DECIMAL_PRICES)
def test_valid_decimal(str_val, expected_val):
    assert scrape_products.str_to_decimal_price(str_val) == Decimal(expected_val)


INVALID_DECIMAL_PRICES = [
    (None),
    (''),
    ('Word'),
    ('-15'),
    ('-2.3'),
]
@pytest.mark.parametrize('str_val', INVALID_DECIMAL_PRICES)
def test_invalid_decimal(str_val):
    assert scrape_products.str_to_decimal_price(str_val) is None


class TestScrapeProducts(TestCase):

    def setUp(self):
        self.currency = Currency.objects.create(name='AUD')
        self.scrape_type_price = ScrapeType.objects.create(name='Price')
        self.store = Store.objects.create(name='Woolworths', currency=self.currency, dynamic_page=False)
        ScrapeTemplate.objects.create(
            store=self.store, scrape_type=self.scrape_type_price,
            xpath=common.TEST_PAGE_WITH_PRICE_20_XPATH)

    def test_dynamic_pages_not_implemented(self):
        self.store.dynamic_page = True
        self.store.save()

        Product.objects.create(store=self.store, prod_url=common.TEST_PAGE_WITH_PRICE_20, name='Tomatoes 20')
        with self.assertRaises(NotImplementedError):
            scrape_products.process_products(0)

    def test_scrape_products_good(self):
        Product.objects.create(store=self.store, prod_url=common.TEST_PAGE_WITH_PRICE_100, name='Tomatoes 100')
        Product.objects.create(store=self.store, prod_url=common.TEST_PAGE_WITH_PRICE_20, name='Tomatoes 20')

        self.assertEqual(ProductPrice.objects.all().count(), 0)
        scrape_products.process_products(0)
        self.assertEqual(ProductPrice.objects.all().count(), 2)

        price_list = ProductPrice.objects.values_list('price', flat=True)
        self.assertListEqual(sorted(price_list), [Decimal('20.00'), Decimal('100.00')])

    def test_scrape_product_invalid_xpath(self):
        Product.objects.create(store=self.store, prod_url=common.TEST_PAGE_WITH_PRICE_20, name='Tomatoes 20')

        template = ScrapeTemplate.objects.filter(store=self.store, scrape_type=self.scrape_type_price).first()
        self.assertEqual(template.xpath, common.TEST_PAGE_WITH_PRICE_20_XPATH)
        template.xpath = common.INVALID_XPATH
        template.save()

        template = ScrapeTemplate.objects.filter(store=self.store, scrape_type=self.scrape_type_price).first()
        self.assertEqual(template.xpath, common.INVALID_XPATH)

        self.assertEqual(ProductPrice.objects.all().count(), 0)
        scrape_products.process_products(0)
        product_prices = ProductPrice.objects.all()
        self.assertEqual(product_prices.count(), 1)

        entry = product_prices.first()
        self.assertIsNone(entry.price)
        self.assertIsNotNone(entry.error)


    def test_scrape_product_url_not_found(self):
        Product.objects.create(store=self.store, prod_url=common.TEST_PAGE_NOT_FOUND, name='Tomatoes 20')

        self.assertEqual(ProductPrice.objects.all().count(), 0)
        scrape_products.process_products(0)
        product_prices = ProductPrice.objects.all()
        self.assertEqual(product_prices.count(), 1)

        entry = product_prices.first()
        print('>>> ENTRY', entry.__dict__)
        self.assertIsNone(entry.price)
        self.assertIsNotNone(entry.error)