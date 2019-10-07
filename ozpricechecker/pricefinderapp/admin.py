from django.contrib import admin
from .models import (
    Currency, Store, StoreProduct, ProductPrice,
    UserProduct, ScrapeType, ScrapeTemplate,
    UserNewsLetter, NewsLetterUserProduct, NewsLetterTime
)


# Register your models here.
admin.site.register(Currency)
admin.site.register(Store)
admin.site.register(StoreProduct)
admin.site.register(ProductPrice)
admin.site.register(UserProduct)
admin.site.register(ScrapeType)
admin.site.register(ScrapeTemplate)

admin.site.register(UserNewsLetter)
admin.site.register(NewsLetterUserProduct)
admin.site.register(NewsLetterTime)
