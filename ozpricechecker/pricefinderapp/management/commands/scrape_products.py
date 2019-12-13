""" Command to scrape Product informatiuon."""

import logging

from django.db import transaction
from django.core.management.base import BaseCommand

from ezscrape.scraping import scraper
from ezscrape.scraping.core import ScrapeConfig
from ezscrape.scraping.core import ScrapeStatus

from pricefinderapp.models import Product, ProductPrice

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Command(BaseCommand):
    """Command Class."""

    def handle(self, *args, **options):
        """Handle the Command."""
        self.scrape_products()

    def scrape_products(self):
        """Scrape the products."""
        '''
        for prod in Product.objects.all():
            full_url = prod.full_url

            !!! if dynamic raise not implemented !!!

            result

            result = scraper.scrape_url(ScrapeConfig(full_url))
            if result.status == ScrapeStatus.SUCCESS:
        '''


def scrape_product(url):
    result_html = None
    error_msg = None

    result = scraper.scrape_url(ScrapeConfig(url))
    if result.status == ScrapeStatus.SUCCESS:
        result_html = result.first_page.html
    else:
        error_msg = result.error_msg

    return (result_html, error_msg)