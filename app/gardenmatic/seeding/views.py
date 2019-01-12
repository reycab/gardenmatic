"""Views Seeding."""
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from app.common.mixins import UserPermissionsRequired
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from django.contrib import messages
from app.gardenmatic.seeding.forms import SeedingForm
from app.gardenmatic import models


class SeedingListView(UserPermissionsRequired, ListView):
    """Listado de Sembradios."""

    model = models.Seeding
    template_name = 'gardenmatic/seeding/list.html'
    paginate_by = 15
    ordering = ['id']

    def get_queryset(self):
        """."""
        queryset = super(SeedingListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset


class SeedingCreateView(UserPermissionsRequired, CreateView):
    """Crear Sembradio."""

    template_name = 'gardenmatic/seeding/create.html'
    model = models.Seeding
    form_class = SeedingForm

    def form_valid(self, form):
        """."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super(SeedingCreateView, self).form_valid(form)

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS, _("Successful creation"))
        return reverse('gardenmatic:seeding-list')

    def form_invalid(self, form):
        """."""
        messages.add_message(
            self.request, messages.ERROR,
            _("Please correct the error below."))
        return self.render_to_response(self.get_context_data(form=form))


class SeedingUpdateView(UserPermissionsRequired, UpdateView):
    """Actualizar Sembradio."""

    template_name = 'gardenmatic/seeding/edit.html'
    model = models.Seeding
    form_class = SeedingForm
    pk_url_kwarg = 'pk'

    def form_valid(self, form):
        """."""
        self.object = form.save(commit=False)
        self.object.save()
        return super(SeedingUpdateView, self).form_valid(form)

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Successful update"))
        if 'save-and-add' in self.request.POST:
            return reverse('gardenmatic:seeding-create')
        else:
            return reverse('gardenmatic:seeding-edit', args=[self.object.id, ])

    def form_invalid(self, form):
        """."""
        messages.add_message(
            self.request, messages.ERROR,
            _("Please correct the error below."))
        return self.render_to_response(self.get_context_data(form=form))


class SeedingDeleteView(UserPermissionsRequired, DeleteView):
    """Eliminar Sembradio."""

    template_name = 'gardenmatic/seeding/delete.html'
    model = models.Seeding
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        """."""
        messages.add_message(
            self.request, messages.SUCCESS,
            _("Successful delete"))
        return reverse('gardenmatic:seeding-list')
