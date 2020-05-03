
import pytest

from utils.scrape import scraper


def test_no_expath_specified():
    with pytest.raises(ValueError):
        scraper.scrape_page(
            chrome='dummy',
            chrome_webdriver='dummy',
            url='dummy',
            xpath_tup_list=[]
        )


def test_duplicate_xpath_name_specified():
    with pytest.raises(ValueError):
        scraper.scrape_page(
            chrome='dummy',
            chrome_webdriver='dummy',
            url='dummy',
            xpath_tup_list=[('name', 'xpath'), ('name', 'xpathw')]
        )
