# -*- coding: utf-8 -*-

"""Modelos de base de datos de GardenMatic."""

from __future__ import unicode_literals
from datetime import datetime, timedelta, time
from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _
from django.db.models import Min, Max


class Seeding(models.Model):
    """."""

    name = models.CharField(
        max_length=50, null=False, blank=False, verbose_name=_('Name'))
    ambient_humidity_min = models.PositiveIntegerField(
        verbose_name=_('Ambient Humidity Min (%)'))
    ambient_humidity_max = models.PositiveIntegerField(
        verbose_name=_('Ambient Humidity Max (%)'))
    ambient_temperature_min = models.PositiveIntegerField(
        verbose_name=_('Ambient Temperature Min (ºC)'))
    ambient_temperature_max = models.PositiveIntegerField(
        verbose_name=_('Ambient Temperature Max (ºC)'))
    sun_time_min = models.PositiveIntegerField(
        verbose_name=_('Sun Time Min (Hours)'))
    sun_time_max = models.PositiveIntegerField(
        verbose_name=_('Sun Time Max (Hours)'))
    user = models.ForeignKey(
        'accounts.user', null=False, blank=False, on_delete=models.CASCADE)
    size = models.PositiveIntegerField(
        verbose_name=_('Size (Meters)'))
    start_time_reading = models.TimeField(
        null=False, blank=False, verbose_name=_('Start Time Reading'))
    end_time_reading = models.TimeField(
        null=False, blank=False, verbose_name=_('End Time Reading'))
    sensing_time = models.PositiveIntegerField(
        null=False, blank=False, verbose_name=_('Sensing Time (Minutes)'))
    opening_time = models.PositiveIntegerField(
        null=False, blank=False, verbose_name=_('Opening Time (Seconds)'))

    class Meta:
        """."""

        db_table = 'seeding'
        verbose_name = _('Seeding')
        verbose_name_plural = _('Seedings')

    def __str__(self):
        """."""
        return '{}'.format(self.name)

    def get_sensores(self):
        """."""
        return self.sensor_set.all()


class Sensor(models.Model):
    """Modelo del Sensor."""

    SOLENOIDE_VALVE = 'solenoide_valve'
    LIGHT = 'light'
    AMBIENT_HUMIDITY = 'ambient_humidity'
    AMBIENT_TEMPERATURE = 'ambient_temperature'
    GROUND_HUMIDITY = 'ground_humidity'

    TYPE_SENSOR_CHOICE = (
        (SOLENOIDE_VALVE, _('Solenoide Valve')),
        (LIGHT, _('Light Sensor')),
        (AMBIENT_HUMIDITY, _('Ambient Humidity')),
        (AMBIENT_TEMPERATURE, _('Ambient Temperature')),
        (GROUND_HUMIDITY, _('Ground Humidity'))
    )

    GPIO_4_7 = 4
    GPIO_5_29 = 5
    GPIO_6_31 = 6
    GPIO_12_32 = 12
    GPIO_13_33 = 13
    GPIO_16_36 = 16
    GPIO_17_11 = 17
    GPIO_18_12 = 18
    GPIO_19_35 = 19
    GPIO_20_38 = 20
    GPIO_21_40 = 21
    GPIO_22_15 = 22
    GPIO_23_16 = 23
    GPIO_24_18 = 24
    GPIO_25_22 = 25
    GPIO_26_37 = 26
    GPIO_27_13 = 27

    GPIO_PHYSICAL_PINS_CHOICE = (
        (GPIO_4_7, _('GPIO 4 (Physical 7)')),
        (GPIO_5_29, _('GPIO 5 (Physical 29)')),
        (GPIO_6_31, _('GPIO 6 (Physical 31)')),
        (GPIO_12_32, _('GPIO 12 (Physical 32)')),
        (GPIO_13_33, _('GPIO 13 (Physical 33)')),
        (GPIO_16_36, _('GPIO 16 (Physical 36)')),
        (GPIO_17_11, _('GPIO 17 (Physical 11)')),
        (GPIO_18_12, _('GPIO 18 (Physical 12)')),
        (GPIO_19_35, _('GPIO 19 (Physical 35)')),
        (GPIO_20_38, _('GPIO 20 (Physical 38)')),
        (GPIO_21_40, _('GPIO 21 (Physical 40)')),
        (GPIO_22_15, _('GPIO 22 (Physical 15)')),
        (GPIO_23_16, _('GPIO 23 (Physical 16)')),
        (GPIO_24_18, _('GPIO 24 (Physical 18)')),
        (GPIO_25_22, _('GPIO 25 (Physical 22)')),
        (GPIO_26_37, _('GPIO 26 (Physical 37)')),
        (GPIO_27_13, _('GPIO 27 (Physical 13)')),
    )

    seeding = models.ForeignKey(
        Seeding, null=False, blank=False, on_delete=models.CASCADE,
        verbose_name=_('Seeding'))
    name = models.CharField(
        max_length=50, null=False, blank=False, verbose_name=_('Name'))
    pin = models.PositiveIntegerField(
        null=False, blank=False, choices=GPIO_PHYSICAL_PINS_CHOICE,
        verbose_name=_('Pin'))
    status = models.BooleanField(default=False, verbose_name=_('Status'))
    type_sensor = models.CharField(
        max_length=25, null=False, blank=False,
        choices=TYPE_SENSOR_CHOICE, verbose_name=_('Type Sensor'))

    class Meta:
        """."""

        db_table = 'sensor'
        verbose_name = _('Sensor')
        verbose_name_plural = _('Sensors')

    def __str__(self):
        """."""
        return '{}({})'.format(self.name, self.get_type_sensor_display())

    def get_today(self):
        """."""
        today = datetime.now()
        tomorrow = today + timedelta(1)
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        return today, today_start, today_end

    def get_lecturas(self):
        """."""
        today, today_start, today_end = self.get_today()
        return self.sensorreading_set.filter(
            date_time__lte=today_end, date_time__gte=today_start)

    def get_luminosidad(self):
        """."""
        tiempo_de_sol = 0

        minutos = self.seeding.sensing_time
        luminosidad = self.get_lecturas().filter(
            sensor__type_sensor=self.LIGHT)

        for lum in luminosidad:
            if lum.reading >= 80:
                tiempo_de_sol = tiempo_de_sol + minutos

        return tiempo_de_sol / 60

    def get_luminosidad_text(self):
        """."""
        tiempo_de_sol = self.get_luminosidad()
        horas = int(tiempo_de_sol)
        tiempo_de_sol = int(tiempo_de_sol * 60)
        minutos = tiempo_de_sol % 60
        if minutos == 0:
            return "{} hora(s)".format(horas)
        if horas > 0:
            return format_html(
                "{} hora(s) <br> {} minutos".format(horas, minutos))
        return "{} minutos".format(minutos)

    def get_nublado(self):
        """."""
        tiempo_de_nublado = 0

        minutos = self.seeding.sensing_time
        luminosidad = self.get_lecturas().filter(
            sensor__type_sensor=self.LIGHT)

        for lum in luminosidad:
            if lum.reading < 80:
                tiempo_de_nublado = tiempo_de_nublado + minutos

        return tiempo_de_nublado / 60

    def get_nublado_text(self):
        """."""
        tiempo_nublado = self.get_nublado()
        horas = int(tiempo_nublado)
        tiempo_nublado = int(tiempo_nublado * 60)
        minutos = tiempo_nublado % 60
        if minutos == 0:
            return "{} hora(s)".format(horas)
        if horas > 0:
            return format_html(
                "{} hora(s) <br>{} minutos".format(horas, minutos))
        return "{} minutos".format(minutos)

    def get_temperatura_ambiental_min(self):
        """."""
        temperatura = self.get_lecturas().filter(
            sensor__type_sensor=self.AMBIENT_TEMPERATURE).aggregate(
                Min('reading'))
        return temperatura['reading__min']

    def get_temperatura_ambiental_max(self):
        """."""
        temperatura = self.get_lecturas().filter(
            sensor__type_sensor=self.AMBIENT_TEMPERATURE).aggregate(
                Max('reading'))
        return temperatura['reading__max']

    def get_humedad_ambiental_min(self):
        """."""
        humedad = self.get_lecturas().filter(
            sensor__type_sensor=self.AMBIENT_HUMIDITY).aggregate(
                Min('reading'))
        return humedad['reading__min']

    def get_humedad_ambiental_max(self):
        """."""
        temperatura = self.get_lecturas().filter(
            sensor__type_sensor=self.AMBIENT_HUMIDITY).aggregate(
                Max('reading'))
        return temperatura['reading__max']

    def get_riegos(self):
        """."""
        riegos = self.get_lecturas().filter(
            sensor__type_sensor=self.SOLENOIDE_VALVE, reading=1).count()
        return riegos


class SensorReading(models.Model):
    """."""

    sensor = models.ForeignKey(
        Sensor, null=False, blank=False, on_delete=models.CASCADE,
        verbose_name=_('Sensor'))
    reading = models.FloatField(verbose_name=_('Reading'))
    date_time = models.DateTimeField(auto_now=True)

    class Meta:
        """."""

        db_table = 'sensor_reading'
        verbose_name = _('Sensor Reading')
        verbose_name_plural = _('Sensors Reading')

    def __str__(self):
        """."""
        return '{}'.format(self.sensor.name)
