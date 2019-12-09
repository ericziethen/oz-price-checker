"""ozpricechecker modesl defination."""

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

    def __str__(self):
        return self.name


class ProductPrice(models.Model):
    """Product price details."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)

    # def __str__(self):
    #     return self.price


class UserProduct(models.Model):
    """User Product details."""

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    threshhold = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        """User Product meta data."""

        unique_together = (('product', 'user'),)


class ScrapeType(models.Model):
    """Product price details."""

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
        """Product price details."""

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
