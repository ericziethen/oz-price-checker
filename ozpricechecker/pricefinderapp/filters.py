"""ozpricechecker filters defination."""

import django_filters
from pricefinderapp.models import UserProduct, ProductPrice
from decimal import Decimal


class UserProductFilter(django_filters.FilterSet):
    """UserProduct filter."""

    price_max = django_filters.NumberFilter(label='PriceMax')

    class Meta:
        """UserProduct filter meta data."""

        model = UserProduct
        # fields = ('product', 'threshhold')
        fields = {
            'product': ['exact'],
            'threshhold': ['lte', 'gt'],
            # 'product.latest_price': ['exact'],
        }

    def __init__(self, *args, **kwargs):
        params = args[0].copy()

        self.price_max = None
        if 'price_max' in params:
            self.price_max = params['price_max']
            del params['price_max']
        new_args = (params,)
        super().__init__(*new_args, **kwargs)


    def filter_queryset(self, queryset):
        filtered_set = super().filter_queryset(queryset)

        if self.price_max:
            wanted_ids = set()
            for user_product in filtered_set:
                if user_product.product.latest_price <= Decimal(self.price_max):
                    wanted_ids.add(user_product.pk)
            return filtered_set.filter(pk__in=wanted_ids)

        return filtered_set
