"""App level view."""

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
