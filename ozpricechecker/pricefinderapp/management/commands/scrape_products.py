""" Command to scrape Product informatiuon."""

import logging
import time

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from django.db import transaction
from django.core.management.base import BaseCommand

from ezscrape.scraping import scraper
from ezscrape.scraping.core import ScrapeConfig
from ezscrape.scraping.core import ScrapeStatus

from defusedxml import lxml as defused_lxml
import lxml

from pricefinderapp.models import Product, ProductPrice, ScrapeTemplate

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Command(BaseCommand):
    """Command Class."""

    def handle(self, *args, **options):
        """Handle the Command."""
        process_products()


def process_products():
    for prod in Product.objects.all():
        xpath_dic = {}

        store = prod.store

        if store.dynamic_page:
            raise NotImplementedError('Need to enable Selenium Scraping to support Dynamic Pages')

        # get all price xpath for now
        for template in ScrapeTemplate.objects.filter(store=prod.store, scrape_type__name='Price'):
            xpath_dic['Price'] = template.xpath

        # Scrape the data
        result_dic = scrape_url(prod.full_url, xpath_dic)
        prod_price = ProductPrice.objects.create(product=prod)

        if 'values' in result_dic:
            if 'value' in result_dic['values']['Price']:
                prod_price.price = str_to_decimal_price(result_dic['values']['Price']['value'])
            else:
                prod_price.error = result_dic['values']['Price']['error']
            prod_price.save()
        else:
            logger.error(F'Scrape Error: {result_dic["error"]}')

        # delay between scrape attempts
        time.sleep(2)


def str_to_decimal_price(str_val):
    result = None

    try:
        val = Decimal(str_val)
    except (InvalidOperation, TypeError):
        result = None
    else:
        if val >= 0.0:
            result = val.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return result



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
