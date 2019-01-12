"""Views gardenmatic."""
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime
from app.common.mixins import UserPermissionsRequired
from rest_framework.decorators import api_view
from django.utils.translation import ugettext_lazy as _
from rest_framework.exceptions import ValidationError
from django.views.generic.base import TemplateView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from . import models
from . import serializers


class HomeView(UserPermissionsRequired, TemplateView):
    """Home View."""

    template_name = "gardenmatic/dashboard.html"

    def get_context_data(self, **kwargs):
        """Get context data."""
        context = super(HomeView, self).get_context_data(**kwargs)
        today = datetime.now()
        configs = models.Seeding.objects.filter(user=self.request.user)
        context['today'] = today
        context['configs'] = configs

        """
        humedad_ambiente = lecturas_hoy.filter(
            sensor_type=models.Sensor.AMBIENT_HUMIDITY)
        temperatura_ambiente = lecturas_hoy.filter(
            sensor_type=models.Sensor.AMBIENT_TEMPERATURE)
        humedad_tierra = lecturas_hoy.filter(
            sensor_type=models.Sensor.GROUND_HUMIDITY)
        """
        return context


class BaseFormView(object):
    """."""

    def get_form(self, form_class=None):
        """."""
        return self.form_class(
            self.request.user, **self.get_form_kwargs())


@api_view(['POST'])
def reading_sensor(request):
    """Servicio para registrar datos de sensores."""
    pin = request.data.get('pin')
    lectura = request.data.get('lectura')
    tipo_sensor = request.data.get('tipo_sensor')

    if not pin:
        raise ValidationError(_('No se especificó un pin'))
    if not lectura:
        raise ValidationError(_('No hay valor de lectura'))
    if not tipo_sensor:
        raise ValidationError(_('No hay valor de tipo de sensor'))

    try:
        sensor = models.Sensor.objects.filter(
            pin=pin, type_sensor=tipo_sensor)

        reading_sensor = models.SensorReading()
        reading_sensor.sensor = sensor[0]
        reading_sensor.reading = lectura
        reading_sensor.save()

        return Response(
            {'message': _('Lectura guardada con exito')},
            status=status.HTTP_200_OK)

    except models.Sensor.DoesNotExist:
        raise ValidationError(_('El pin del sensor no está registrado'))


class SensoresDisponiblesApiViewSet(viewsets.ModelViewSet):
    """."""

    queryset = models.Sensor.objects.all()
    serializer_class = serializers.SensorSerializer
    allowed_methods = ('GET',)

    def list(self, request, *args, **kwargs):
        """."""
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(status=True)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
