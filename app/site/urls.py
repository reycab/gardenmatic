"""."""
from __future__ import unicode_literals

from django.urls import path
from app.site import views

app_name = 'site'

urlpatterns = [
    path(r'', views.HomeView.as_view(), name='home'),
]
