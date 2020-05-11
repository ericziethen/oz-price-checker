"""ozpricechecker filters defination."""

from decimal import Decimal
import django_filters
from pricefinderapp.models import UserProduct


class UserProductFilter(django_filters.FilterSet):
    """UserProduct filter."""

    price_max = django_filters.NumberFilter(label='PriceMax')
    # price_date_from = django_filters.DateTimeFilter(label='From Price Date')
    # price_date_to = django_filters.DateTimeFilter(label='To Price Date')
    price_date = django_filters.DateTimeFromToRangeFilter(label='Price Date')

    class Meta:
        """UserProduct filter meta data."""

        model = UserProduct
        # fields = ('product', 'threshhold')
        fields = {
            'product': ['exact'],
            'threshhold': ['lte', 'gte'],
        }

    def __init__(self, *args, **kwargs):
        """Override initialization of product filter."""
        params = args[0].copy()

        self.price_max = None
        if 'price_max' in params:
            self.price_max = params['price_max']
            del params['price_max']
        new_args = (params,)
        super().__init__(*new_args, **kwargs)

    def filter_queryset(self, queryset):
        """Override filter for product."""
        filtered_set = super().filter_queryset(queryset)

        if self.price_max:
            wanted_ids = set()
            for user_product in filtered_set:
                if user_product.product.latest_price <= Decimal(self.price_max):
                    wanted_ids.add(user_product.pk)
            return filtered_set.filter(pk__in=wanted_ids)

        return filtered_set
