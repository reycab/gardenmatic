"""."""
from rest_framework import serializers
from . import models


class SensorSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        """."""

        model = models.Sensor
        fields = ('pin', 'type_sensor')
