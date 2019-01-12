"""Views site."""
# -*- encoding: utf-8 -*-

from __future__ import unicode_literals

from django.views.generic.base import TemplateView


class HomeView(TemplateView):
    """Home View."""

    template_name = "site/home.html"
