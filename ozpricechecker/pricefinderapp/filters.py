"""ozpricechecker filters defination."""

import django_filters
from pricefinderapp.models import UserProduct, ProductPrice
from decimal import Decimal





class MyFilter(django_filters.filters.Filter):

    def filter(self, qs, value):
        print('MyFilter.filter', value, qs)
        filtered_qs = super().filter(qs, value)
        print('MyFilter.filter, filtered', value, filtered_qs)
        return filtered_qs


class MyNumberFilter(django_filters.filters.NumberFilter):

    def filter(self, qs, value):

        #print('MyFilter.filter', value, qs)
        #filtered_qs = super().filter(qs, value)
        #print('MyFilter.filter, filtered', value, filtered_qs)
        #return filtered_qs

        if value is not None:
            wanted_ids = set()
            for user_product in qs:
                if user_product.product.latest_price <= value:
                    wanted_ids.add(user_product.pk)
            return qs.filter(pk__in=wanted_ids)

        return qs
# TODO - Generalize the Filter so we can easily use it for different Properties without less code
# e.g. We can pass extra info to the Init Function


class UserProductFilter(django_filters.FilterSet):
    """UserProduct filter."""

    #price_max = django_filters.NumberFilter(label='PriceMax')
    #price_max = MyFilter(label='PriceMax')

    price_max = MyNumberFilter(label='PriceMax <=')

    class Meta:
        """UserProduct filter meta data."""

        model = UserProduct
        # fields = ('product', 'threshhold')
        fields = {
            'product': ['exact'],
            'threshhold': ['lte', 'gt'],
            # 'product.latest_price': ['exact'],
        }

    '''
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
    '''