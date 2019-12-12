"""App level URL mapping."""

<<<<<<< HEAD
from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='userproduct_list', permanent=False), name='home'),
    path('userproduct/', views.UserProductListView.as_view(), name='userproduct_list'),
=======
from django.conf.urls import url
# from django.views.generic import TemplateView
from pricefinderapp.views import UserProductListView
# from . import views


urlpatterns = [
    # url('', TemplateView.as_view(template_name='index.html'), name='home'),
    # url('', views.index, name='home'),
    url('', UserProductListView.as_view(), name='user_products'),
>>>>>>> Home page list view
]
