"""Manage the Admin Interface."""

from django.contrib import admin
from .forms import StoreCreateForm
from .models import (
    Currency, Store, Product, ProductPrice,
    UserProduct, ScrapeType, ScrapeTemplate,
    UserNewsLetter, NewsLetterUserProduct, NewsLetterTime
)


class StoreAdmin(admin.ModelAdmin):
    """Admin model for Store."""

    form = StoreCreateForm

    list_display = ('name', 'prod_base_url', 'currency', 'dynamic_page')
    list_filter = ('currency__name', 'dynamic_page')


# Register your models here.
admin.site.register(Currency)
admin.site.register(Store, StoreAdmin)
admin.site.register(Product)
admin.site.register(ProductPrice)
admin.site.register(UserProduct)
admin.site.register(ScrapeType)
admin.site.register(ScrapeTemplate)

admin.site.register(UserNewsLetter)
admin.site.register(NewsLetterUserProduct)
admin.site.register(NewsLetterTime)
