"""Test Scraper Functionality."""

from tests import common
from utils.scrape import scraper


def test_page_found():
    result = scraper.scrape_url(common.TEST_PAGE_WITH_PRICE_20)
    assert result[0] is not None
    assert result[1] is None


def test_page_not_found():
    result = scraper.scrape_url(common.TEST_PAGE_NOT_FOUND)
    assert result[0] is None
    assert result[1] is not None
