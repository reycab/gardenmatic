# coding=utf-8
"""Sensor Forms."""
from __future__ import unicode_literals

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from app.gardenmatic.models import SensorReading, Sensor


class SensorReadingForm(forms.ModelForm):
    """."""

    helper = FormHelper()
    helper.method = 'POST'
    helper.form_tag = False
    helper.html5_required = True
    helper.layout = Layout(
        Div('sensor', css_class="col-md-4"),
        Div('reading', css_class="col-md-4"),
        Div(css_class="row"),
    )

    class Meta:
        """Meta class."""

        model = SensorReading
        exclude = []

    def __init__(self, user, *args, **kwargs):
        """."""
        self.user = user
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['sensor'].queryset = Sensor.objects.filter(
            seeding__user=self.user)
