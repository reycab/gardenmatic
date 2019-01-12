"""Admin."""
from django.contrib import admin

from . import models


admin.site.register(models.Seeding)
admin.site.register(models.Sensor)


@admin.register(models.SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    """."""

    list_display = ['sensor', 'reading', 'date_time']
