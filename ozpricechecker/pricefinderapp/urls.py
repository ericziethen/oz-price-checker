"""App level URL mapping."""

from django.conf.urls import url
from django.views.generic import TemplateView


urlpatterns = [
    url('', TemplateView.as_view(template_name='index.html'), name='home'),
]
