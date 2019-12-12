"""App level view."""
<<<<<<< HEAD

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from pricefinderapp.models import UserProduct


class UserProductListView(LoginRequiredMixin, ListView):  # pylint: disable=too-many-ancestors
    """User product list view."""

    model = UserProduct
    paginate_by = 100
    template_name = 'pricefinderapp/userproduct_list.html'

    def get_queryset(self):
        """Only for current user."""
        return UserProduct.objects.filter(user=self.request.user)
=======

# from django.shortcuts import render
from django.views.generic.list import ListView
from pricefinderapp.models import UserProduct


class UserProductListView(ListView):
    """User product list view."""

    model = UserProduct
    paginate_by = 100


# def index(request):
#     """View function for home page of site."""
#     user_products = UserProduct.objects.all()
#     print(user_products)
#     return render(request, 'index.html', {'user_products': user_products})
>>>>>>> Home page list view
