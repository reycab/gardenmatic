"""."""

from django.urls import path, include

from . import views

app_name = 'gardenmatic'


urlpatterns = [
    path(r'', views.HomeView.as_view(), name='home'),
    path(r'seeding/', include('app.gardenmatic.seeding.urls')),
    path(r'sensor/', include('app.gardenmatic.sensor.urls')),
    path(r'sensor-reading/', include('app.gardenmatic.sensor_reading.urls')),
]
