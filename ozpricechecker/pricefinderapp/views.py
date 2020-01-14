"""App level view."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
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
    model = UserProduct
    template_name = 'pricefinderapp/userproduct_add.html'
    fields = ('product', 'threshhold', )
    success_url = reverse_lazy('userproduct_list')


class UserProductUpdateView(LoginRequiredMixin, UpdateView): 
    model = UserProduct
    template_name = 'pricefinderapp/userproduct_update.html'
    fields = ('threshhold', )
    context_object_name = 'UserProduct'
    success_url = reverse_lazy('userproduct_list')

    # def get_success_url(self):
    #     return reverse_lazy('userproduct_list', kwargs={'pk': self.object.id})


class UserProducttDeleteView(DeleteView): 
    model = UserProduct