# coding=utf-8
"""Sensor Forms."""
from __future__ import unicode_literals

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from app.gardenmatic.models import Sensor, Seeding
from django.utils.translation import ugettext_lazy as _


class SensorForm(forms.ModelForm):
    """."""

    helper = FormHelper()
    helper.method = 'POST'
    helper.form_tag = False
    helper.html5_required = True
    helper.layout = Layout(
        Div('seeding', css_class="col-md-4"),
        Div('pin', css_class="col-md-4"),
        Div('type_sensor', css_class="col-md-4"),
        Div(css_class="row"),
        Div('name', css_class="col-md-8"),
        Div(css_class="row"),
        Div('status', css_class="col-md-4"),
        Div(css_class="row"),
    )

    class Meta:
        """Meta class."""

        model = Sensor
        exclude = []

    def clean(self):
        """Validate date."""
        cleaned_data = super(SensorForm, self).clean()

        pin = cleaned_data['pin']
        type_sensor = cleaned_data['type_sensor']
        sensors = Sensor.objects.filter(pin=pin)
        pk = self.instance.pk
        if pk:
            sensors = sensors.exclude(pk=pk)

        if sensors:
            for sensor in sensors:
                if sensor.type_sensor in (sensor.AMBIENT_HUMIDITY, sensor.AMBIENT_TEMPERATURE):  # noqa
                    if sensor.type_sensor == type_sensor or type_sensor not in (sensor.AMBIENT_HUMIDITY, sensor.AMBIENT_TEMPERATURE):  # noqa
                        raise forms.ValidationError(
                            {'pin': _('El pin ya está en uso')})
                else:
                    raise forms.ValidationError(
                        {'pin': _('El pin ya está en uso')})
        return cleaned_data

    def __init__(self, user, *args, **kwargs):
        """."""
        self.user = user
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['seeding'].queryset = Seeding.objects.filter(
            user=self.user)
        choice = Sensor.objects.values_list('pin', flat=True).distinct()
        self.fields['pin'].choices = [
            (o, p) for o, p in Sensor.GPIO_PHYSICAL_PINS_CHOICE
            if o not in choice]
