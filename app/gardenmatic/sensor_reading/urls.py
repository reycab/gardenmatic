"""."""

from django.urls import path

from . import views

urlpatterns = [
    path(
        r'', views.SensorReadingListView.as_view(),
        name='sensor-reading-list'),
    path(
        r'create', views.SensorReadingCreateView.as_view(),
        name='sensor-reading-create'),
    path(
        r'edit/<int:pk>', views.SensorReadingUpdateView.as_view(),
        name="sensor-reading-edit"),
    path(
        r'delete/<int:pk>', views.SensorReadingDeleteView.as_view(),
        name="sensor-reading-delete"),
]
