
from ezscrape.scraping import scraper
from ezscrape.scraping.core import ScrapeConfig
from ezscrape.scraping.core import ScrapeStatus


def scrape_url(url):
    """Scrape the online Product url."""
    result_html = None
    error_msg = None

    result = scraper.scrape_url(ScrapeConfig(url))
    if result.status == ScrapeStatus.SUCCESS:
        result_html = result.first_page.html
    else:
        error_msg = result.error_msg

    return (result_html, error_msg)
