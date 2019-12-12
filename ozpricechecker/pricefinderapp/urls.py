"""App level URL mapping."""

from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='userproduct_list', permanent=False), name='home'),
    path('userproduct/', views.UserProductListView.as_view(), name='userproduct_list'),
]
