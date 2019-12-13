import pytest

from decimal import Decimal

from django.test import TestCase

from pricefinderapp.models import Currency, Product, ScrapeTemplate, ScrapeType, Store
from pricefinderapp.management.commands import scrape_products
from tests import common


def test_page_found():
    result = scrape_products.scrape_product_url(common.TEST_PAGE_WITH_PRICE_20)
    assert result[0] is not None
    assert result[1] is None


def test_page_not_found():
    result = scrape_products.scrape_product_url(common.TEST_PAGE_NOT_FOUND)
    assert result[0] is None
    assert result[1] is not None


def test_get_price_from_html():
    xpath = common.TEST_PAGE_WITH_PRICE_20_XPATH
    price = scrape_products.get_xpath_from_html(xpath, common.HTML_WITH_PRICE)
    assert price == '20'


def test_price_not_in_html():
    xpath = '//price-not-found/text()'
    price = scrape_products.get_xpath_from_html(xpath, common.HTML_WITH_PRICE)
    assert price is None


def test_invalid_xpath():
    with pytest.raises(ValueError):
        scrape_products.get_xpath_from_html(common.INVALID_XPATH, common.HTML_WITH_PRICE)


def test_no_xpath_values_specified():
    with pytest.raises(ValueError):
        scrape_products.scrape_url(common.TEST_PAGE_NOT_FOUND, {})


def test_invalid_url():
    xpath_dic = {
        'price': common.TEST_PAGE_WITH_PRICE_20_XPATH,
        'price-not-found': '//price-not-found/text()',
        'invalid_xpath': common.INVALID_XPATH
    }
    result = scrape_products.scrape_url(common.TEST_PAGE_NOT_FOUND, xpath_dic)

    assert 'values' not in result
    assert result['error']


def test_price_from_url():
    xpath_dic = {
        'price': common.TEST_PAGE_WITH_PRICE_20_XPATH,
        'price-not-found': '//price-not-found/text()',
        'invalid_xpath': common.INVALID_XPATH
    }
    result = scrape_products.scrape_url(common.TEST_PAGE_WITH_PRICE_20, xpath_dic)

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
def test_valid_decimal(str_val):
    assert scrape_products.str_to_decimal_price(str_val) is None


class TestScrapeProducts(TestCase):

    def setUp(self):
        self.currency = Currency.objects.create(name='AUD')
        self.scrape_type_price = ScrapeType.objects.create(name='Price')
        self.store = Store.objects.create(name='Woolworths', currency=self.currency, dynamic_page=True)
        ScrapeTemplate.objects.create(
            store=self.store, scrape_type=self.scrape_type_price,
            xpath=common.TEST_PAGE_WITH_PRICE_20_XPATH)

    @pytest.mark.eric
    def test_dynamic_pages_not_implemented(self):
        self.store.dynamic_page = True
        self.store.save()

        Product.objects.create(store=self.store, prod_url=common.TEST_PAGE_WITH_PRICE_20, name='Dynamic Tomatoes')
        with self.assertRaises(NotImplementedError):
            scrape_products.process_products()


    '''
    def test_scrape_products_good(self):
        self.assertFalse(True)

    def test_scrape_product_invalid_xpath(self):
        self.assertFalse(True)

    def test_scrape_product_url_not_found(self):
        self.assertFalse(True)
    '''
    '''
    @pytest.mark.eric
    def test_dynamic_pages_not_supported():
        with pytest
    '''
