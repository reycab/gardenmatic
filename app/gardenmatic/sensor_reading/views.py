"""Views gardenmatic."""
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from app.common.mixins import AdminPermissionsRequired
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from app.gardenmatic.sensor_reading.forms import SensorReadingForm
from app.gardenmatic import models
from app.gardenmatic.views import BaseFormView


class SensorReadingListView(AdminPermissionsRequired, ListView):
    """Listado de Lecturas de sensores."""

    model = models.SensorReading
    template_name = 'gardenmatic/sensor_reading/list.html'
    paginate_by = 15
    ordering = ['id']

    def get_queryset(self):
        """."""
        queryset = super(SensorReadingListView, self).get_queryset()
        return queryset


class SensorReadingCreateView(
        AdminPermissionsRequired, BaseFormView, CreateView):
    """Crear Lectura de sensor."""

    template_name = 'gardenmatic/sensor_reading/create.html'
    model = models.SensorReading
    form_class = SensorReadingForm

    def form_valid(self, form):
        """."""
        self.object = form.save(commit=False)
        self.object.save()
        return super(SensorReadingCreateView, self).form_valid(form)

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS, _("Successful creation"))
        return reverse('gardenmatic:sensor-reading-list')

    def form_invalid(self, form):
        """."""
        messages.add_message(
            self.request, messages.ERROR,
            _("Please correct the error below."))
        return self.render_to_response(self.get_context_data(form=form))


class SensorReadingUpdateView(
        AdminPermissionsRequired, BaseFormView, UpdateView):
    """Update Lectura de sensor."""

    template_name = 'gardenmatic/sensor_reading/edit.html'
    model = models.SensorReading
    form_class = SensorReadingForm
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        """."""
        self.object = form.save(commit=False)
        self.object.save()
        return super(SensorReadingUpdateView, self).form_valid(form)

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Successful update"))
        if 'save-and-add' in self.request.POST:
            return reverse('gardenmatic:sensor-reading-create')
        else:
            return reverse(
                'gardenmatic:sensor-reading-edit', args=[self.object.id, ])

    def form_invalid(self, form):
        """."""
        messages.add_message(
            self.request, messages.ERROR,
            _("Please correct the error below."))
        return self.render_to_response(self.get_context_data(form=form))


class SensorReadingDeleteView(AdminPermissionsRequired, DeleteView):
    """Eliminar lectura de sensor."""

    template_name = 'gardenmatic/sensor_reading/delete.html'
    model = models.SensorReading
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Successful delete"))
        return reverse('gardenmatic:sensor-reading-list')
