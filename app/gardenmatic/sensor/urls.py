"""."""

from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.SensorListView.as_view(), name='sensor-list'),
    path(
        r'create', views.SensorCreateView.as_view(),
        name='sensor-create'),
    path(
        r'edit/<int:pk>', views.SensorUpdateView.as_view(),
        name="sensor-edit"),
    path(
        r'delete/<int:pk>', views.SensorDeleteView.as_view(),
        name="sensor-delete"),
]
