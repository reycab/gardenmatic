# -*- encoding: utf-8 -*-
"""Model."""

from __future__ import unicode_literals

import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """User model."""

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email', ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=100, verbose_name=_('Last Name'))
    image = models.ImageField(
        default=settings.DEFAULT_USER_IMAGE, blank=True,
        verbose_name=_('Image'))
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    force_change_password = models.BooleanField(default=True)

    objects = UserManager()

    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        """Meta class."""

        db_table = 'auth_user'

    def __str__(self):
        """."""
        if self.first_name or self.last_name:
            return self.get_full_name()
        return self.email

    def get_full_name(self):
        """."""
        fullname = '{} {}'.format(self.first_name, self.last_name)
        if fullname.strip() == '':
            return self.email
        return fullname

    def get_short_name(self):
        """."""
        return self.email

    @property
    def is_staff(self):
        """Return True if user is staff."""
        return self.is_admin

    @property
    def full_name(self):
        """Return user full name."""
        return self.get_full_name()

    def reset_password(self):
        """Generate and return a new passwordl."""
        password = uuid.uuid4().hex[:6].upper()
        self.set_password(password)
        self.force_change_password = True
        self.save()
        return password
