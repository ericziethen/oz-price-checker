from decimal import Decimal

import pytest

from django.test import TestCase

from pricefinderapp.models import (
    Currency, Product, ProductPrice, ScrapeTemplate, ScrapeType, Store
)
from pricefinderapp.management.commands import scrape_products
from tests import common


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

    def test_scrape_full_price_ok(self):
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
        self.assertEqual(ProductPrice.objects.all().count(), 0)

    def test_scrape_product_url_not_found(self):
        Product.objects.create(store=self.store, prod_url=common.TEST_PAGE_NOT_FOUND, name='Tomatoes 20')

        self.assertEqual(ProductPrice.objects.all().count(), 0)
        scrape_products.process_products(0)
        self.assertEqual(ProductPrice.objects.all().count(), 0)


class TestScrapeProductsWithSplitPrice(TestCase):

    def setUp(self):
        self.currency = Currency.objects.create(name='AUD')
        self.scrape_type_price_whole_num = ScrapeType.objects.create(name='PriceWholeNumber')
        self.scrape_type_price_fraction = ScrapeType.objects.create(name='PriceFraction')
        self.store = Store.objects.create(name='Woolworths', currency=self.currency, dynamic_page=False)

    def test_scrape_whole_price_only(self):
        ScrapeTemplate.objects.create(
            store=self.store, scrape_type=self.scrape_type_price_whole_num,
            xpath=common.TEST_PAGE_WITH_PRICE_12_95_XPATH_WHOLE)

        Product.objects.create(store=self.store, prod_url=common.TEST_PAGE_WITH_PRICE_12_95,
                               name='Tomatoes 12.95')
        self.assertEqual(ProductPrice.objects.all().count(), 0)
        scrape_products.process_products(0)
        self.assertEqual(ProductPrice.objects.all().count(), 1)

        price_list = ProductPrice.objects.values_list('price', flat=True)
        self.assertListEqual(sorted(price_list), [Decimal('12.00')])

    def test_scrape_fraction_price_only(self):
        ScrapeTemplate.objects.create(
            store=self.store, scrape_type=self.scrape_type_price_fraction,
            xpath=common.TEST_PAGE_WITH_PRICE_12_95_XPATH_FRACTION)

        Product.objects.create(store=self.store, prod_url=common.TEST_PAGE_WITH_PRICE_12_95,
                               name='Tomatoes 12.95')
        self.assertEqual(ProductPrice.objects.all().count(), 0)
        scrape_products.process_products(0)
        self.assertEqual(ProductPrice.objects.all().count(), 1)

        price_list = ProductPrice.objects.values_list('price', flat=True)
        self.assertListEqual(sorted(price_list), [Decimal('0.95')])

    def test_scrape_whole_and_fraction_price(self):
        ScrapeTemplate.objects.create(
            store=self.store, scrape_type=self.scrape_type_price_whole_num,
            xpath=common.TEST_PAGE_WITH_PRICE_12_95_XPATH_WHOLE)
        ScrapeTemplate.objects.create(
            store=self.store, scrape_type=self.scrape_type_price_fraction,
            xpath=common.TEST_PAGE_WITH_PRICE_12_95_XPATH_FRACTION)

        Product.objects.create(store=self.store, prod_url=common.TEST_PAGE_WITH_PRICE_12_95,
                               name='Tomatoes 12.95')
        self.assertEqual(ProductPrice.objects.all().count(), 0)
        scrape_products.process_products(0)
        self.assertEqual(ProductPrice.objects.all().count(), 1)

        price_list = ProductPrice.objects.values_list('price', flat=True)
        self.assertListEqual(sorted(price_list), [Decimal('12.95')])
