"""Command to scrape Product informatiuon."""

import logging
import os
import time

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation

from django.core.management.base import BaseCommand, CommandError

from pricefinderapp.models import Product, ProductPrice, ScrapeTemplate

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

        process_products(5, chrome_exec_path=chrome_exec_path, chrome_webdriver_path=chrome_webdriver_path)


def process_products(scrape_delay_seconds, *, chrome_exec_path, chrome_webdriver_path):
    """Process the products with the given delay."""
    for prod in Product.objects.all():

        # Get the Xpath List for Price
        xpath_tup_list = get_price_xpaths(prod)

        # Scrape the Price
        result = scraper.scrape_page(
            chrome=chrome_exec_path,
            chrome_webdriver=chrome_webdriver_path,
            url=prod.full_url,
            xpath_tup_list=xpath_tup_list
        )

        # Process Price Data
        process_price_scrape_result(prod, result)

        # Sleep
        time.sleep(scrape_delay_seconds)


def get_price_xpaths(prod):
    """Get the Xpath list for Times to Scrape."""
    xpath_tup_list = []

    # Check full Price Xpath
    full_price_xpath = get_xpath_for_scrape_type(prod, 'Price')
    if full_price_xpath:
        xpath_tup_list.append(('Price', full_price_xpath))

    # Check Partial Price Xpath
    whole_xpath = get_xpath_for_scrape_type(prod, 'PriceWholeNumber')
    fraction_xpath = get_xpath_for_scrape_type(prod, 'PriceFraction')
    if whole_xpath and fraction_xpath:
        xpath_tup_list.append(('PriceWholeNumber', whole_xpath))
        xpath_tup_list.append(('PriceFraction', fraction_xpath))

    return xpath_tup_list


def get_xpath_for_scrape_type(prod, scrape_type):
    """Get the Xpath for a specific Scrape Type."""
    xpath = None
    template = ScrapeTemplate.objects.filter(store=prod.store, scrape_type__name=scrape_type).first()

    if template:
        xpath = template.xpath

    return xpath


def process_price_scrape_result(prod, result):
    """Process the result of the Price Scrape."""
    price_str = ''

    if 'Price' in result:
        price_str = result['Price']
    elif 'PriceWholeNumber' in result and 'PriceFraction' in result:
        price_str = F'''{result['PriceWholeNumber']}.{result['PriceFraction']}'''

    if price_str:
        price = str_to_decimal_price(price_str)

        if price:
            ProductPrice.objects.create(product=prod, price=price)
        else:
            logger.error(F'Failed to convert "{price_str}" to Decimal')
    else:
        logger.error(F'No Price found for Product: "{prod}"')


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
