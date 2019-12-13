import ezscrape.scraping.scraper as scraper

from .common import LOCAL_SERVER_HTTP


def test_local_test_server_running():
    assert scraper.check_url(LOCAL_SERVER_HTTP, local_only=True)
