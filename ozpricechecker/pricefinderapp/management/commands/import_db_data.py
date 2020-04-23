"""Command to Handle Import Data from CSV Files."""

import csv
import logging
import os

from collections import OrderedDict

from django.db import transaction
from django.core.management.base import BaseCommand, CommandError
from pricefinderapp.models import (
    Currency, Product, ScrapeType, ScrapeTemplate, Store
)

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Command(BaseCommand):
    """The Base Command."""

    def add_arguments(self, parser):
        """Add command line arguments."""
        parser.add_argument('base_path', type=str)

    def handle(self, *args, **options):
        """Handle the command."""
        base_path = options['base_path']

        # Supported files to import
        import_files = OrderedDict()

        import_files[os.path.join(base_path, 'currencies.csv')] = self.populate_currencies
        import_files[os.path.join(base_path, 'stores.csv')] = self.populate_stores
        import_files[os.path.join(base_path, 'scrape_types.csv')] = self.populate_scrape_types
        import_files[os.path.join(base_path, 'scrape_templates.csv')] = self.populate_scrape_templates
        import_files[os.path.join(base_path, 'products.csv')] = self.populate_products

        try:
            self.validate_base_path(base_path, import_files.keys())
        except ValueError as error:
            raise CommandError(F'Failed to validate config path: {error}')

        # Process import files
        for file_path, import_func in import_files.items():
            with open(file_path, encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                import_func(reader)

    @staticmethod
    def validate_base_path(base_path, expected_file_list):
        """Validate the base path."""
        # Check path exists as directory
        if not os.path.exists(base_path) or not os.path.isdir(base_path):
            raise ValueError(F'"{base_path}" is not a valid Directory Path')

        # Check all expected files are present
        for file_path in expected_file_list:
            if not os.path.exists(file_path):
                raise ValueError(F'Expected file "{file_path}" not found')

    @staticmethod
    def populate_currencies(csv_data):
        """Populate Currency db."""
        logger.info(F'Populate Currencies')
        with transaction.atomic():
            for row in csv_data:
                Currency.objects.update_or_create(name=row['ISO'])

    @staticmethod
    def populate_stores(csv_data):
        """Populate Store db."""
        logger.info(F'Populate Stores')
        with transaction.atomic():
            for row in csv_data:
                Store.objects.update_or_create(
                    name=row['Name'],
                    prod_base_url=row['Base Url'],
                    dynamic_page=row['Dynamic Page'].lower() == 'true',
                    currency=Currency.objects.get(name=row['Currency'])
                )

    @staticmethod
    def populate_scrape_types(csv_data):
        """Populate Scrape Type db."""
        logger.info(F'Populate Scrape Types')
        with transaction.atomic():
            for row in csv_data:
                ScrapeType.objects.update_or_create(name=row['Name'])

    @staticmethod
    def populate_scrape_templates(csv_data):
        """Populate Scrape Template db."""
        logger.info(F'Populate Scrape Templates')
        with transaction.atomic():
            for row in csv_data:
                ScrapeTemplate.objects.update_or_create(
                    store=Store.objects.get(name=row['Store']),
                    scrape_type=ScrapeType.objects.get(name=row['Scrape Type']),
                    xpath=row['Xpath'],
                )

    @staticmethod
    def populate_products(csv_data):
        """Populate Product db."""
        logger.info(F'Populate Products')
        with transaction.atomic():
            for row in csv_data:
                Product.objects.update_or_create(
                    store=Store.objects.get(name=row['Store']),
                    prod_url=row['Product Url'],
                    name=row['Product Name']
                )
