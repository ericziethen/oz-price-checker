from django.test import TestCase

from pricefinderapp.models import ScrapeType


class SetupTests(TestCase):

    def test_str(self):
        scrape_type = ScrapeType.objects.create(name='price')
        self.assertEqual(str(scrape_type), 'price')
