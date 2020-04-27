
import pytest

from tests import common
from utils.htmlparse import xpathparser


def test_get_price_from_html():
    xpath = common.TEST_PAGE_WITH_PRICE_20_XPATH
    price = xpathparser.get_xpath_from_html(xpath, common.HTML_WITH_PRICE)
    assert price == '20'


def test_price_not_in_html():
    xpath = '//price-not-found/text()'
    price = xpathparser.get_xpath_from_html(xpath, common.HTML_WITH_PRICE)
    assert price is None


def test_invalid_xpath():
    with pytest.raises(ValueError):
        xpathparser.get_xpath_from_html(common.INVALID_XPATH, common.HTML_WITH_PRICE)
