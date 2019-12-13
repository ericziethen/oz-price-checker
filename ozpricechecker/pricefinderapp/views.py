"""App level view."""

from django.views.generic.list import ListView
from pricefinderapp.models import UserProduct


class UserProductListView(ListView):
    """User product list view."""

    model = UserProduct
    paginate_by = 100
    template_name = 'pricefinderapp/userproduct_list.html'

    def get_queryset(self):
        """Only for current user."""
        return UserProduct.objects.filter(user=self.request.user)
