# coding=utf-8
"""Seeding Forms."""
from __future__ import unicode_literals

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from app.gardenmatic.models import Seeding


class SeedingForm(forms.ModelForm):
    """."""

    helper = FormHelper()
    helper.method = 'POST'
    helper.form_tag = False
    helper.layout = Layout(
        Div('name', css_class="col-lg-3 col-md-6 col-sm-12"),
        Div('size', css_class="col-lg-3 col-md-6 col-sm-12"),
        Div('ambient_humidity_min', css_class="col-lg-3 col-md-6 col-sm-12"),
        Div('ambient_humidity_max', css_class="col-lg-3 col-md-6 col-sm-12"),
        Div(css_class="row"),
        Div(
            'ambient_temperature_min',
            css_class="col-lg-3 col-md-6 col-sm-12"),
        Div(
            'ambient_temperature_max',
            css_class="col-lg-3 col-md-6 col-sm-12"),
        Div('sun_time_min', css_class="col-lg-3 col-md-6 col-sm-12"),
        Div('sun_time_max', css_class="col-lg-3 col-md-6 col-sm-12"),
        Div(css_class="row"),
        Div('start_time_reading', css_class="col-lg-3 col-md-6 col-sm-12"),
        Div('end_time_reading', css_class="col-lg-3 col-md-6 col-sm-12"),
        Div('sensing_time', css_class="col-lg-3 col-md-6 col-sm-12"),
        Div('opening_time', css_class="col-lg-3 col-md-6 col-sm-12"),
        Div(css_class="row"),
    )

    class Meta:
        """Meta class."""

        model = Seeding
        exclude = ['user', ]

    def __init__(self, *args, **kwargs):
        """."""
        super(self.__class__, self).__init__(*args, **kwargs)
