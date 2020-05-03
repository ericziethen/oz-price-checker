
from decimal import Decimal
from pathlib import Path

import pytest

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from pricefinderapp.management.commands import scrape_products

VALID_FILE_PATH = Path('ozpricechecker') / 'pricefinderapp' / '__init__.py'
INVALID_FILE_PATH = 'this-is-not-a-path'

VALID_DECIMAL_PRICES = [
    ('0', '0.00'),
    ('0.0', '0.00'),
    ('0.1', '0.10'),
    ('1', '1.00'),
    ('1.0', '1.00'),
    ('15.23', '15.23'),
    ('15.234', '15.23'),
    ('15.235', '15.24'),
    ('15.236', '15.24'),
]
@pytest.mark.parametrize('str_val, expected_val', VALID_DECIMAL_PRICES)
def test_valid_decimal(str_val, expected_val):
    assert scrape_products.str_to_decimal_price(str_val) == Decimal(expected_val)


INVALID_DECIMAL_PRICES = [
    (None),
    (''),
    ('Word'),
    ('-15'),
    ('-2.3'),
]
@pytest.mark.parametrize('str_val', INVALID_DECIMAL_PRICES)
def test_invalid_decimal(str_val):
    assert scrape_products.str_to_decimal_price(str_val) is None


class CommandArgumentTestCase(TestCase):

    def test_no_argument_given(self):  # pylint: disable=no-self-use
        with pytest.raises(CommandError):
            args = []
            opts = {}
            call_command('scrape_products', *args, **opts)

    def test_only_single_argument_given(self):  # pylint: disable=no-self-use
        with pytest.raises(CommandError):
            args = [VALID_FILE_PATH]
            opts = {}
            call_command('scrape_products', *args, **opts)

    def test_first_arg_invalid_path(self):  # pylint: disable=no-self-use
        with pytest.raises(CommandError):
            args = [INVALID_FILE_PATH, VALID_FILE_PATH]
            opts = {}
            call_command('scrape_products', *args, **opts)

    def test_second_arg_invalid_path(self):  # pylint: disable=no-self-use
        with pytest.raises(CommandError):
            args = [VALID_FILE_PATH, INVALID_FILE_PATH]
            opts = {}
            call_command('scrape_products', *args, **opts)

    def test_2_valid_path(self):  # pylint: disable=no-self-use
        args = [VALID_FILE_PATH, VALID_FILE_PATH]
        opts = {}
        call_command('scrape_products', *args, **opts)
