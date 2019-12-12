"""App level URL mapping."""

from django.conf.urls import url
# from django.views.generic import TemplateView
from pricefinderapp.views import UserProductListView
# from . import views


urlpatterns = [
    # url('', TemplateView.as_view(template_name='index.html'), name='home'),
    # url('', views.index, name='home'),
    url('', UserProductListView.as_view(), name='user_products'),
]
