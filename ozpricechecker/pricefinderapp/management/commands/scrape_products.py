"""Command to scrape Product informatiuon."""

import logging
import os
import time

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from django.core.management.base import BaseCommand, CommandError

from pricefinderapp.models import Product, ProductPrice, ScrapeTemplate

from utils.htmlparse import xpathparser
from utils.scrape import scraper

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Command(BaseCommand):
    """Command Class."""

    def add_arguments(self, parser):
        """Add command line arguments."""
        parser.add_argument('chrome_exec_path', type=str)
        parser.add_argument('chrome_webdriver_path', type=str)

    def handle(self, *args, **options):
        """Handle the Command."""
        chrome_exec_path = options['chrome_exec_path']
        chrome_webdriver_path = options['chrome_webdriver_path']

        if not os.path.exists(chrome_exec_path) or not os.path.exists(chrome_webdriver_path):
            raise CommandError('Need to Specify [chrome_exec_path] and [chrome_webdriver_path]')

        process_products(5)


def process_products(scrape_delay, *, chrome_exec_path=None, chrome_webdriver_path=None):
    """Process the products with the given delay."""
    for prod in Product.objects.all():

        store = prod.store

        # If chrome execs passed force selenium mode
        if chrome_exec_path and chrome_webdriver_path:
            store.dynamic_page = True
            os.environ['CHROME_EXEC_PATH'] = chrome_exec_path
            os.environ['CHROME_WEBDRIVER_PATH'] = chrome_webdriver_path

        # Scrape the Product Page
        prod_url = prod.full_url
        html_source, error_msg = scraper.scrape_url(prod_url)

        if html_source:
            # Scrape Price Data
            parse_produc_price(prod, html_source)

            # delay between scrape attempts
            time.sleep(scrape_delay)

        else:
            logger.error(F'Failed to Scrape Product "{prod} - Url: {prod_url}, Error: {error_msg}')


def parse_produc_price(db_prod, html_source):
    """Parse the Product Prices."""
    price_str = None

    # Parse the Full Price
    price_str = parse_template(db_prod, 'Price', html_source)

    # Parse the Partial Price
    if not price_str:
        whole_str = parse_template(db_prod, 'PriceWholeNumber', html_source)
        fraction_str = parse_template(db_prod, 'PriceFraction', html_source)

        price_str = F'{whole_str}.{fraction_str}'

    if price_str:
        price = str_to_decimal_price(price_str)

        if price:
            ProductPrice.objects.create(product=db_prod, price=price)
        else:
            logger.error(F'Failed to convert "{price_str}" to Decimal')
    else:
        logger.error(F'No Price found for Product: "{db_prod}"')


def parse_template(prod, scrape_type, html):
    """Parse the template."""
    result = ''
    template = ScrapeTemplate.objects.filter(store=prod.store, scrape_type__name=scrape_type).first()

    if template:
        try:
            result = xpathparser.get_xpath_from_html(template.xpath, html)
        except ValueError as error:
            logger.error(F'Failed to parse xpath: "{template.xpath}" for Product: {prod} - Error: {error}')

    return result


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
