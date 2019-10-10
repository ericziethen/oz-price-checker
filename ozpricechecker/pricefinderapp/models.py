from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=30, unique=True)
    prod_base_url = models.TextField(unique=True)
    dynamic_page = models.BooleanField(default=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    prod_url = models.TextField(unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    # def __str__(self):
    #     return self.price


class UserProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    threshhold = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = (('product', 'user'),)


class ScrapeType(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class ScrapeTemplate(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    scrape_type = models.ForeignKey(ScrapeType, on_delete=models.CASCADE)
    xpath = models.TextField(unique=True)

    def __str__(self):
        return self.xpath


class UserNewsLetter(models.Model):
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

    def __str__(self):
        return self.name


class NewsLetterUserProduct(models.Model):
    user_newsletter_id = models.ForeignKey(UserNewsLetter, on_delete=models.CASCADE)
    user_product = models.ForeignKey(UserProduct, on_delete=models.CASCADE)


class NewsLetterTime(models.Model):
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
