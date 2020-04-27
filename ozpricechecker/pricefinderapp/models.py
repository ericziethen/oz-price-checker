"""ozpricechecker models defination."""

from decimal import Decimal
from urllib.parse import urljoin

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Currency(models.Model):
    """Currency master."""

    name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    """Store master."""

    name = models.CharField(max_length=30, unique=True)
    prod_base_url = models.TextField(unique=True)
    dynamic_page = models.BooleanField(default=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Product master."""

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    prod_url = models.TextField()
    name = models.CharField(max_length=30)

    class Meta:
        """Product meta data."""

        unique_together = (('store', 'prod_url'),)

    @property
    def full_url(self):
        """Get the full url for this product."""
        base_url = self.store.prod_base_url
        if not base_url.endswith('/'):
            base_url += '/'
        return urljoin(base_url, self.prod_url)

    @property
    def latest_price(self):
        """Get latest price for this product."""
        product_price = ProductPrice.objects.filter(product=self).order_by('-date_time').first()
        if product_price:
            return product_price.price
        return None

    @property
    def date_for_latest_price(self):
        """Get the latest price date for this product."""
        product_price = ProductPrice.objects.filter(product=self).order_by('-date_time').first()
        if product_price:
            return product_price.date_time
        return None

    def __str__(self):
        return '%s - %s' % (self.store, self.name)


class ProductPrice(models.Model):
    """Product price details."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    price = models.DecimalField(
        max_digits=12, blank=True, null=True, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))])
    error = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        """ProductPrice meta data."""

        unique_together = (('product', 'date_time'),)


class UserProduct(models.Model):
    """User Product details."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    threshhold = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        """User Product meta data."""

        ordering = ['-id']
        unique_together = (('product', 'user'),)

    @property
    def is_threshhold_reached(self):
        """Get if threshold reached for this product."""
        product_price = ProductPrice.objects.filter(product=self.product).order_by('-date_time').first()
        if product_price and product_price.price <= self.threshhold:
            return True
        return False


class ScrapeType(models.Model):
    """Scrape type master."""

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class ScrapeTemplate(models.Model):
    """Defines scraping templates for store."""

    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    scrape_type = models.ForeignKey(ScrapeType, on_delete=models.CASCADE)
    xpath = models.TextField()

    class Meta:
        """Scraping Template meta data."""

        unique_together = (('store', 'scrape_type'),)

    def __str__(self):
        return self.xpath


class UserNewsLetter(models.Model):
    """User news letter configuration."""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, unique=True)

    # DEFINED = 'DF'
    # UNDEFINED = 'UD'
    # NEWS_LETTER_CHOICES = [
    #     (DEFINED, 'defined'),
    #     (UNDEFINED, 'undefined'),
    # ]
    # state = models.CharField(
    #     max_length=2,
    #     choices=NEWS_LETTER_CHOICES,
    #     default=UNDEFINED,
    # )

    class Meta:
        """UserNewsLetter meta data."""

        unique_together = (('user', 'name'),)

    def __str__(self):
        return self.name


class NewsLetterUserProduct(models.Model):
    """Product configuration of user news letter."""

    user_newsletter = models.ForeignKey(UserNewsLetter, on_delete=models.CASCADE)
    user_product = models.ForeignKey(UserProduct, on_delete=models.CASCADE)

    class Meta:
        """NewsLetterUserProduct meta data."""

        unique_together = (('user_newsletter', 'user_product'),)


class NewsLetterTime(models.Model):
    """News letter notification time configuration."""

    user_newsletter = models.ForeignKey(UserNewsLetter, on_delete=models.CASCADE)
    # pylint: disable=invalid-name
    MONDAY = 'MON'
    TUESDAY = 'TUE'
    WEDNESDAY = 'WED'
    THURSDAY = 'THR'
    FRIDAY = 'FRI'
    STATURDAY = 'SAT'
    SUNDAY = 'SUN'
    WEEKDAY_CHOICES = [
        (MONDAY, 'monday'),
        (TUESDAY, 'tuesday'),
        (WEDNESDAY, 'wednesday'),
        (THURSDAY, 'thursday'),
        (FRIDAY, 'friday'),
        (STATURDAY, 'staturday'),
        (SUNDAY, 'sunday'),
    ]
    week_day = models.CharField(
        max_length=3,
        choices=WEEKDAY_CHOICES,
        default=MONDAY,
    )
    time = models.TimeField()
