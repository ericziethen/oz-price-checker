"""App level URL mapping."""

from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('', RedirectView.as_view(pattern_name='userproduct_list', permanent=False), name='home'),
    path('userproduct/', views.UserProductListView.as_view(), name='userproduct_list'),
    path('adduserproduct/', views.UserProductCreateView.as_view(), name='userproduct_add'),
    path('update/<int:pk>', views.UserProductUpdateView.as_view(), name='userproduct_update'),
    path('delete/<int:pk>', views.UserProducttDeleteView.as_view(), name='userproduct_delete'),
]
