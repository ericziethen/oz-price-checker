"""ozpricechecker filters defination."""

import django_filters
from django import forms
from pricefinderapp.models import UserProduct


class DateInput(forms.DateInput):
    """Date picker wadget."""

    input_type = 'date'


class CustDateRangeWidget(django_filters.widgets.SuffixedMultiWidget):
    """Custome date picker wadget."""

    template_name = 'django_filters/widgets/multiwidget.html'
    suffixes = ['after', 'before']

    def __init__(self, attrs=None):
        """Initialize to date range."""
        widgets = (DateInput, DateInput)
        super().__init__(widgets, attrs)

    def decompress(self, value):
        """Decompose."""
        if value:
            return slice(value.start, value.stop)
        return slice(None, None)


class CustomNumberFilter(django_filters.filters.NumberFilter):
    """Custome number filter."""

    def filter(self, qs, value):
        """Filter for custom number."""
        # print(self.lookup_expr)
        if value is not None:
            wanted_ids = set()
            if self.lookup_expr == 'lte':
                for user_product in qs:
                    if user_product.product.latest_price <= value:
                        wanted_ids.add(user_product.pk)
                return qs.filter(pk__in=wanted_ids)
            if self.lookup_expr == 'gte':
                for user_product in qs:
                    if user_product.product.latest_price >= value:
                        wanted_ids.add(user_product.pk)
                return qs.filter(pk__in=wanted_ids)
            if self.lookup_expr == 'exact':
                for user_product in qs:
                    if user_product.product.latest_price == value:
                        wanted_ids.add(user_product.pk)
                return qs.filter(pk__in=wanted_ids)
        return qs


class CustomDateFromToRangeFilter(django_filters.filters.DateFromToRangeFilter):
    """Custome date time range filter."""

    def filter(self, qs, value):
        """Filter for custom from to date range."""
        if value:
            wanted_ids = set()
            if value.start is not None and value.stop is not None:
                for user_product in qs:
                    if user_product.product.date_for_latest_price >= value.start and \
                       user_product.product.date_for_latest_price <= value.stop:
                        wanted_ids.add(user_product.pk)
                return qs.filter(pk__in=wanted_ids)
            if value.start is not None:
                for user_product in qs:
                    if user_product.product.date_for_latest_price >= value.start:
                        wanted_ids.add(user_product.pk)
                return qs.filter(pk__in=wanted_ids)
            if value.stop is not None:
                for user_product in qs:
                    if user_product.product.date_for_latest_price <= value.stop:
                        wanted_ids.add(user_product.pk)
                return qs.filter(pk__in=wanted_ids)
        return qs


class UserProductFilter(django_filters.FilterSet):
    """UserProduct filter."""

    threshhold_gte = django_filters.NumberFilter(label='Price Threshhold >=',
                                                 field_name='threshhold', lookup_expr='gte')
    threshhold_lte = django_filters.NumberFilter(label='Price Threshhold <=',
                                                 field_name='threshhold', lookup_expr='lte')
    price_min = CustomNumberFilter(label='Price >=', lookup_expr='gte')
    price_max = CustomNumberFilter(label='Price <=', lookup_expr='lte')
    price_date = CustomDateFromToRangeFilter(label='Price Date Range', widget=CustDateRangeWidget())

    class Meta:
        """UserProduct filter meta data."""

        model = UserProduct
        fields = {
            'product': ['exact'],
        }
