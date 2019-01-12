"""Admin."""
from django.contrib import admin
from django.contrib.auth import admin as admin_auth

from . import models


@admin.register(models.User)
class UserAdmin(admin_auth.UserAdmin):
    """User Admin."""

    list_display = (
        'email', 'first_name',
        'last_name', 'is_superuser')
    list_filter = ('is_active', )
    fieldsets = (
        (None, {
            'fields': (
                'email', 'password',
                'first_name', 'last_name', 'is_active',
                'is_admin', 'is_superuser'
            )
        }),
        ('Permissions', {'fields': ('groups', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('groups',)
