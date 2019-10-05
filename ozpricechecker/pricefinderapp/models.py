# from enum import Enum
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "currency"


class Store(models.Model):
    name = models.CharField(max_length=30)
    prod_base_url = models.CharField(max_length=250)
    dynamic_page = models.BooleanField(default=False)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "Store"


class StoreProduct(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    prod_url = models.CharField(max_length=250)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "StoreProduct"


class ProductPrice(models.Model):
    store_prod_id = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now=True)
    price = models.IntegerField()

    # def __str__(self):
    #     return self.price

    class Meta:
        db_table = "ProductPrice"


class UserProduct(models.Model):
    store_prod_id = models.ForeignKey(StoreProduct, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    threshhold = models.IntegerField()

    class Meta:
        db_table = "Userproduct"


class ScrapeType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ScrapeType"


class ScrapeTemplate(models.Model):
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    scrape_type = models.ForeignKey(ScrapeType, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "ScrapeTemplate"


class UserNewsLetter(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)

    DEFINED = 'DF'
    UNDEFINED = 'UD'
    NEWS_LETTER_CHOICES = [
        (DEFINED, 'defined'),
        (UNDEFINED, 'undefined'),
    ]
    state = models.CharField(
        max_length=2,
        choices=NEWS_LETTER_CHOICES,
        default=UNDEFINED,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "UserNewsLetter"


class NewsLetterUserProduct(models.Model):
    user_newsletter_id = models.ForeignKey(UserNewsLetter, on_delete=models.CASCADE)
    user_product_id = models.ForeignKey(UserProduct, on_delete=models.CASCADE)

    class Meta:
        db_table = "NewsLetterUserProduct"


class NewsLetterTime(models.Model):
    user_newsletter_id = models.ForeignKey(UserNewsLetter, on_delete=models.CASCADE)

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
