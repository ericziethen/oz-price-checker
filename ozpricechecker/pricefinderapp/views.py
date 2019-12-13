"""App level view."""

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from pricefinderapp.models import UserProduct


class UserProductListView(ListView):  # pylint: disable=too-many-ancestors
    """User product list view."""

    model = UserProduct
    paginate_by = 100
    template_name = 'pricefinderapp/userproduct_list.html'

    def get_queryset(self):
        """Only for current user."""
        return UserProduct.objects.filter(user=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Relogin if user not logged in."""
        return super(UserProductListView, self).dispatch(*args, **kwargs)
