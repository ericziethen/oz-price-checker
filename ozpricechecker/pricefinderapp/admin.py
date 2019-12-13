"""Manage the Admin Interface."""

from django.contrib import admin
from .forms import StoreCreateForm
from .models import (
    Currency, Store, Product, ProductPrice,
    UserProduct, ScrapeType, ScrapeTemplate,
    UserNewsLetter, NewsLetterUserProduct, NewsLetterTime
)


class ProductPriceAdmin(admin.ModelAdmin):
    """Admin model for ProductPrice."""

    list_display = ('product', 'date_time', 'price', 'error')


class ScrapeTemplateAdmin(admin.ModelAdmin):
    """Admin model for ScrapeTemplate."""

    list_display = ('store', 'scrape_type', 'xpath')
    list_filter = ('store', 'scrape_type')


class StoreAdmin(admin.ModelAdmin):
    """Admin model for Store."""

    form = StoreCreateForm

    list_display = ('name', 'prod_base_url', 'currency', 'dynamic_page')
    list_filter = ('currency__name', 'dynamic_page')


# Register your models here.
admin.site.register(Currency)
admin.site.register(Store, StoreAdmin)
admin.site.register(Product)
admin.site.register(ProductPrice, ProductPriceAdmin)
admin.site.register(UserProduct)
admin.site.register(ScrapeType)
admin.site.register(ScrapeTemplate, ScrapeTemplateAdmin)

admin.site.register(UserNewsLetter)
admin.site.register(NewsLetterUserProduct)
admin.site.register(NewsLetterTime)
