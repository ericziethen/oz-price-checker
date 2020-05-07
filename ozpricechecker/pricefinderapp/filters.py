"""ozpricechecker filters defination."""

import django_filters
from pricefinderapp.models import UserProduct


class UserProductFilter(django_filters.FilterSet):
    """UserProduct filter."""

    class Meta:
        """UserProduct filter meta data."""

        model = UserProduct
        # fields = ('product', 'threshhold')
        fields = {
            'product': ['exact'],
            'threshhold': ['lte', 'gt'],
            # 'product.latest_price': ['exact'],
        }
