import pytest

from django.test import TestCase

from pricefinderapp.models import Currency, Product, Store
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
    xpath = '//price/text()'
    price = scrape_products.get_xpath_from_html(xpath, common.HTML_WITH_PRICE)
    assert price == '20'


def test_price_not_in_html():
    xpath = '//price-not-found/text()'
    price = scrape_products.get_xpath_from_html(xpath, common.HTML_WITH_PRICE)
    assert price is None


def test_invalid_xpath():
    with pytest.raises(ValueError):
        scrape_products.get_xpath_from_html('invalid-xpath/', common.HTML_WITH_PRICE)


def test_no_xpath_values_specified():
    with pytest.raises(ValueError):
        scrape_products.scrape_url(common.TEST_PAGE_NOT_FOUND, {})


def test_invalid_url():
    xpath_dic = {
        'price': '//price/text()',
        'price-not-found': '//price-not-found/text()',
        'invalid_xpath': 'invalid-xpath/'
    }
    result = scrape_products.scrape_url(common.TEST_PAGE_NOT_FOUND, xpath_dic)

    assert 'values' not in result
    assert result['error']


def test_price_from_url():
    xpath_dic = {
        'price': '//price/text()',
        'price-not-found': '//price-not-found/text()',
        'invalid_xpath': 'invalid-xpath/'
    }
    result = scrape_products.scrape_url(common.TEST_PAGE_WITH_PRICE_20, xpath_dic)

    print('RESULT', result)

    assert result['values']['price']['value'] == '20'
    assert 'error' not in result['values']['price']

    assert result['values']['price-not-found']['value'] is None
    assert 'error' not in result['values']['price']

    assert 'value' not in result['values']['invalid_xpath']
    assert result['values']['invalid_xpath']['error']


class TestScrapeProducts(TestCase):

    def test_dynamic_pages_not_implemented(self):
        self.assertFalse(True)

    def test_scrape_product(self):
        self.assertFalse(True)




    '''
    @pytest.mark.eric
    def test_dynamic_pages_not_supported():
        with pytest
    '''
