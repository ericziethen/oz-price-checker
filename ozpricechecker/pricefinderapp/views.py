"""App level view."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.http import HttpResponse
from pricefinderapp.models import UserProduct


class UserProductListView(LoginRequiredMixin, ListView):  # pylint: disable=too-many-ancestors
    """User product list view."""

    model = UserProduct
    paginate_by = 100
    template_name = 'pricefinderapp/userproduct_list.html'

    def get_queryset(self):
        """Only for current user."""
        return UserProduct.objects.filter(user=self.request.user)


class UserProductCreateView(LoginRequiredMixin, CreateView):
    """User product create view."""

    model = UserProduct
    template_name = 'pricefinderapp/userproduct_add.html'
    fields = ('product', 'threshhold', )
    success_url = reverse_lazy('userproduct_list')

    def form_valid(self, form):
        """Validate form data."""
        form.instance.user = self.request.user
        try:
            return super().form_valid(form)
        except IntegrityError:
            return HttpResponse("ERROR: User Product already exists!")


class UserProductUpdateView(LoginRequiredMixin, UpdateView):
    """User product update view."""

    model = UserProduct
    template_name = 'pricefinderapp/userproduct_update.html'
    fields = ('threshhold', )
    context_object_name = 'UserProduct'
    success_url = reverse_lazy('userproduct_list')


class UserProducttDeleteView(LoginRequiredMixin, DeleteView):
    """User product delete view."""

    model = UserProduct
    template_name = 'pricefinderapp/userproduct_delete.html'
    context_object_name = 'UserProduct'
    success_url = reverse_lazy('userproduct_list')
