"""."""

from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.SeedingListView.as_view(), name='seeding-list'),
    path(
        r'create', views.SeedingCreateView.as_view(),
        name='seeding-create'),
    path(
        r'edit/<int:pk>', views.SeedingUpdateView.as_view(),
        name="seeding-edit"),
    path(
        r'delete/<int:pk>', views.SeedingDeleteView.as_view(),
        name="seeding-delete"),
]
