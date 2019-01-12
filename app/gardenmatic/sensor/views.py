"""Views gardenmatic."""
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from app.common.mixins import UserPermissionsRequired
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from app.gardenmatic.sensor.forms import SensorForm
from app.gardenmatic import models
from app.gardenmatic.views import BaseFormView


class SensorListView(UserPermissionsRequired, ListView):
    """Listado de Sensores."""

    model = models.Sensor
    template_name = 'gardenmatic/sensor/list.html'
    paginate_by = 15
    ordering = ['id']

    def get_queryset(self):
        """."""
        queryset = super(SensorListView, self).get_queryset()
        queryset = queryset.filter(seeding__user=self.request.user)
        return queryset


class SensorCreateView(UserPermissionsRequired, BaseFormView, CreateView):
    """Crear Sensor."""

    template_name = 'gardenmatic/sensor/create.html'
    model = models.Sensor
    form_class = SensorForm

    def form_valid(self, form):
        """."""
        self.object = form.save(commit=False)
        self.object.save()
        return super(SensorCreateView, self).form_valid(form)

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS, _("Successful creation"))
        return reverse('gardenmatic:sensor-list')

    def form_invalid(self, form):
        """."""
        messages.add_message(
            self.request, messages.ERROR,
            _("Please correct the error below."))
        return self.render_to_response(self.get_context_data(form=form))


class SensorUpdateView(UserPermissionsRequired, BaseFormView, UpdateView):
    """Update Sensor."""

    template_name = 'gardenmatic/sensor/edit.html'
    model = models.Sensor
    form_class = SensorForm
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        """."""
        self.object = form.save(commit=False)
        self.object.save()
        return super(SensorUpdateView, self).form_valid(form)

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Successful update"))
        if 'save-and-add' in self.request.POST:
            return reverse('gardenmatic:sensor-create')
        else:
            return reverse('gardenmatic:sensor-edit', args=[self.object.id, ])

    def form_invalid(self, form):
        """."""
        messages.add_message(
            self.request, messages.ERROR,
            _("Please correct the error below."))
        return self.render_to_response(self.get_context_data(form=form))


class SensorDeleteView(UserPermissionsRequired, DeleteView):
    """Eliminar sensor."""

    template_name = 'gardenmatic/sensor/delete.html'
    model = models.Sensor
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Successful delete"))
        return reverse('gardenmatic:sensor-list')
