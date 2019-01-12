# coding=utf-8
"""Forms."""
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from allauth.account.adapter import get_adapter
from allauth.account.forms import LoginForm, SignupForm, \
    ChangePasswordForm, ResetPasswordForm
from allauth.account.forms import ResetPasswordKeyForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML
from crispy_forms.bootstrap import Div, Field
from allauth.account.utils import (
    setup_user_email)


class CustomLoginForm(LoginForm):
    """Custom login form."""

    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Div(
            Field('login', css_class="input100"),
            HTML("""<span class="focus-input100"></span>"""),
            css_class="wrap-input100 validate-input m-b-20"
        ),
        Div(
            Field('password', css_class="input100"),
            HTML("""<span class="focus-input100"></span>"""),
            css_class="wrap-input100 validate-input m-b-20"
        )
    )

    def __init__(self, *args, **kwargs):
        """Custom login form.

        Args:
            *args (TYPE): Description
            **kwargs (TYPE): Description
        """
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget.attrs['autocomplete'] = 'email'
        self.fields['password'].widget.attrs['autocomplete'] = 'password'

    def login(self, request, redirect_url=None):
        """Login function of form."""
        ret = super(CustomLoginForm, self).login(request, redirect_url)
        return ret


class CustomSignupForm(SignupForm):
    """Custom login form."""

    first_name = forms.CharField(
        max_length=50, label=_('First name'),
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    last_name = forms.CharField(max_length=50, label=_('Last name'))

    helper = FormHelper()
    helper.html5_required = True
    helper.form_tag = False
    helper.layout = Layout(
        Div(
            Div('first_name', css_class="col-md-6 col-sm-12"),
            Div('last_name', css_class="col-md-6 col-sm-12"),
            css_class="row"),
        Div(
            Div('email', css_class="col-12"),
            css_class="row"),
        Div(
            Div('password1', css_class="col-md-6 col-sm-12"),
            Div('password2', css_class="col-md-6 col-sm-12"),
            css_class="row"),
    )

    def __init__(self, *args, **kwargs):
        """Custom login form."""
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.pop('placeholder', None)
        self.fields['password1'].widget.attrs.pop('placeholder', None)
        self.fields['password2'].widget.attrs.pop('placeholder', None)

    def save(self, request):
        """Save."""
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user

    def custom_signup(self, request, user):
        """Custom login form."""
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.is_active = True
        user.save()


class CustomResetPasswordForm(ResetPasswordForm):
    """Reset Password Form."""

    helper = FormHelper()
    helper.form_tag = False


class CustomResetPasswordKeyForm(ResetPasswordKeyForm):
    """Reset Password with Key Form."""

    helper = FormHelper()
    helper.form_tag = False


class CustomChangePasswordForm(ChangePasswordForm):
    """Change Password Form."""

    helper = FormHelper()
    helper.form_tag = False
