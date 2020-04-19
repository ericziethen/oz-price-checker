"""Command to scrape Product informatiuon."""

import logging
import time

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from django.core.management.base import BaseCommand

from ezscrape.scraping import scraper
from ezscrape.scraping.core import ScrapeConfig
from ezscrape.scraping.core import ScrapeStatus

import lxml  # nosec
import lxml.html  # nosec
import lxml.etree  # nosec

from pricefinderapp.models import Product, ProductPrice, ScrapeTemplate

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Command(BaseCommand):
    """Command Class."""

    def handle(self, *args, **options):
        """Handle the Command."""
        process_products(5)


def process_products(scrape_delay):
    """Process the products with the given delay."""
    for prod in Product.objects.all():
        xpath_dic = {}

        store = prod.store

        if store.dynamic_page:
            raise NotImplementedError('Need to enable Selenium Scraping to support Dynamic Pages')

        # get all price xpath for now
        for template in ScrapeTemplate.objects.filter(store=prod.store, scrape_type__name='Price'):
            xpath_dic['Price'] = template.xpath

        # Scrape the data
        result_dic = process_url(prod.full_url, xpath_dic)
        prod_price = ProductPrice.objects.create(product=prod)

        if 'values' in result_dic:
            if 'value' in result_dic['values']['Price']:
                prod_price.price = str_to_decimal_price(result_dic['values']['Price']['value'])
            else:
                prod_price.error = result_dic['values']['Price']['error']
        else:
            prod_price.error = result_dic["error"]
            logger.error(F'Scrape Error: {result_dic["error"]}')

        prod_price.save()

        # delay between scrape attempts
        time.sleep(scrape_delay)


def str_to_decimal_price(str_val):
    """Convert a String to a decimal Price."""
    result = None

    try:
        val = Decimal(str_val)
    except (InvalidOperation, TypeError):
        result = None
    else:
        if val >= 0.0:
            result = val.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    return result


def process_url(url, xpath_dic):
    """Scrape the url and retrieve the xpath values."""
    logger.info(F'Scraping Url: "{url}"')
    result_dic = {}

    if not xpath_dic:
        raise ValueError('No Xpath specified for this scrape')

    # Scrape the URL
    html_source, error_msg = scrape_product_url(url)
    if html_source:
        html_decoded_string = html_source

        result_dic['values'] = {}

        # Process the Scrape Result
        for name, xpath in xpath_dic.items():
            result_dic['values'][name] = {}
            try:
                result = get_xpath_from_html(xpath, html_decoded_string)
            except ValueError as error:
                result_dic['values'][name]['error'] = str(error)
            else:
                result_dic['values'][name]['value'] = result
    else:
        result_dic['error'] = error_msg

    return result_dic


def scrape_product_url(url):
    """Scrape the online Product url."""
    result_html = None
    error_msg = None

    result = scraper.scrape_url(ScrapeConfig(url))
    if result.status == ScrapeStatus.SUCCESS:
        result_html = result.first_page.html
    else:
        error_msg = result.error_msg

    return (result_html, error_msg)


def get_xpath_from_html(xpath, html_source):
    """Get the xpath value from the given html."""
    # logger.info(F'get_xpath_from_html Xpath: {xpath} HTML:\n">>>>>{html_source}<<<<<"')
    try:
        # pylint: disable=c-extension-no-member
        root = lxml.etree.fromstring(html_source)  # nosec
        # pylint: enable=c-extension-no-member
        result = root.xpath(xpath)
    except (lxml.etree.XPathEvalError, lxml.etree.XMLSyntaxError) as error:  # pylint: disable=c-extension-no-member
        raise ValueError(F'Xpath Error for "{xpath}" - {type({error})}: {error}')
    else:
        if result:
            return result[0]

    return None
