import pytest

from pricefinderapp.management.commands import scrape_products
from tests import common


def test_page_found():
    result = scrape_products.scrape_product(common.TEST_PAGE_WITH_PRICE)
    assert result[0] is not None
    assert result[1] is None


def test_page_not_found():
    result = scrape_products.scrape_product(common.TEST_PAGE_NOT_FOUNT)
    assert result[0] is None
    assert result[1] is not None


"""

def test_get_price_from_html()

def test_price_not_in_html()

def test_price_from_local_file()

def test_dynamic_pages_not_supported()
"""


