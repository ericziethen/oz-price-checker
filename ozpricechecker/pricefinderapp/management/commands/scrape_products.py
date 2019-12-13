""" Command to scrape Product informatiuon."""

import logging

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
    scrape_type_fields = {
        'Price': 'price'
    }
    '''
    for prod in Product.objects.all():

        xpath_dic = {}
        # get all xpath we support
        for template in ScrapeTemplate.objects.filter(store=prod.store):
            if template.scrape_type.name in scrape_type_fields:
                xpath_dic[template.scrape_type.name] = template.xpath

        # Scrape the data
        result_dic = scrape_url(prod.full_url, xpath_dic)
        prod_price = ProductPrice.objects.create(product=prod)

        if 'values' in result_dic:
            for name, result in result_dic['values'].items():
                if 'value' in result:
                    pass
                else:
                    pass
        else:
            logger.error(F'Scrape Error: {result["error"]}')



        for result in result_dic:
            if 'values' in result:
                update = True
                if 'value' in result['values'][]

                
                setattr(prod_price, scrape_type_fields[result], )
                prod_price

            else:
                logger.error(F'Scrape Error: {result["error"]}')

        if update:
            prod_price.save()

    # TODO - add to db

    # TODO - add a scrape delay
    '''


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
