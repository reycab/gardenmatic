# -*- coding: utf-8 -*-
"""Provee clases especificas de permisos para los usuarios."""

from __future__ import unicode_literals
from django.urls import reverse
from django.contrib.auth.mixins import PermissionRequiredMixin


class AdminPermissionsRequired(PermissionRequiredMixin):
    """Valida que el usuario logueado tenga permisos de administrador y esté activo."""  # noqa

    def has_permission(self):
        """."""
        if not self.request.user.is_authenticated:
            return False
        if not self.request.user.is_authenticated or not self.request.user.is_active:  # noqa
            if not self.request.user.is_admin:
                self.login_url = ""
            return False
        if not self.request.user.is_admin:
            self.login_url = reverse('gardenmatic:home')
            return False
        return self.request.user.is_admin or self.request.user.is_superuser


class UserPermissionsRequired(PermissionRequiredMixin):
    """Valida que el usuario esté logueado."""

    def has_permission(self):
        """."""
        if not self.request.user.is_authenticated:
            return False
        if self.request.user.is_admin:
            self.login_url = ""
            return True
        return self.request.user.is_active
