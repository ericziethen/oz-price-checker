""" Command to scrape Product informatiuon."""

import logging

from django.db import transaction
from django.core.management.base import BaseCommand

from ezscrape.scraping import scraper
from ezscrape.scraping.core import ScrapeConfig
from ezscrape.scraping.core import ScrapeStatus

from defusedxml import lxml as defused_lxml
import lxml

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


def process_products():
    for prod in Product.objects.all():
        result_dic = scrape_url(prod.full_url)


    # TODO - add to db


def scrape_url(url, xpath_dic):
    result_dic = {}

    if not xpath_dic:
        raise ValueError('No Xpath specified for this scrape')

    # Scrape the URL
    html, error_msg = scrape_product_url(url)
    if html:
        result_dic['values'] = {}

        # Process the Scrape Result
        for name, xpath in xpath_dic.items():
            result_dic['values'][name] = {}
            try:
                result = get_xpath_from_html(xpath, html)
            except ValueError as error:
                result_dic['values'][name]['error'] = str(error)
            else:
                result_dic['values'][name]['value'] = result
    else:
        result_dic['error'] = error_msg

    return result_dic


def scrape_product_url(url):
    result_html = None
    error_msg = None

    result = scraper.scrape_url(ScrapeConfig(url))
    if result.status == ScrapeStatus.SUCCESS:
        result_html = result.first_page.html
    else:
        error_msg = result.error_msg

    return (result_html, error_msg)


def get_xpath_from_html(xpath, html):
    root = defused_lxml.fromstring(html)

    try:
        result = root.xpath(xpath)
    except lxml.etree.XPathEvalError as error:
        raise ValueError(F'Xpath Error for "{xpath}" - {error}')
    else:
        if result:
            return result[0]

    return None
