# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from phonenumber_field.formfields import PhoneNumberField

from .models import Profile

User = get_user_model()


def validate_email_unique(value):
    exists = User.objects.filter(email=value)
    if exists:
        raise ValidationError(_(u'This email address already exists.'))


def check_email(value):
    exists = User.objects.filter(email=value)
    if not exists:
        raise ValidationError(_(u'This email does not exists.'))


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('Username/Email'), }))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': _('Password'), }))

    error_messages = {
        'invalid_login': _("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive or your account has been blocked."),
        'inactive': _("This account is inactive."),
        '': _("This account is inactive."),
    }

class BusinessCreationForm(forms.Form):
    city          = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control placeholder newone arabdir' }))
    country       = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control placeholder newone arabdir' }))
    name          = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control placeholder newone arabdir' }))
    business_type = forms.ChoiceField(required=True, choices=(('shop',_('shop owner')),('server',_('unloking server owner'))), widget=forms.Select(
        attrs={'class': 'form-control placeholder newone arabdir', 'disabled':True}))

class BusinessTypeForm(forms.Form):
    business_type = forms.ChoiceField(required=True, choices=(('',''),('shop',_('shop owner')),('server',_('unloking server owner'))), widget=forms.Select(
        attrs={'class': 'form-control ', 'placeholder':_('Select your business type') }))


class ResetPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('email'), }), validators=[check_email])


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email_unique], widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'email'}))
    username = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username' }))

    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'first name'}))

    last_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'last name'}))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password' }))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password confirmation' }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password1', 'password2', 'groups')


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'first name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'last name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'email'}))

    class Meta:
        model = Profile
        fields = (
            'first_name', 'last_name', 'email', 'phone',)
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': '+212612345678', 'required': 'required'}),
        }


class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'old password', }))
    new_password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'new password', }))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'confirm password', }))


class NewUserForm(SignupForm):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={
                             'class': 'form-control', 'placeholder': '+212612345678', 'required': 'required'}))
    groups = forms.CharField(widget=forms.Select(attrs={
                             'class': 'form-control'}, choices=((1,"Administrator"),(2,"Technician"),(3,"Worker") )))
                             # 'class': 'form-control'}, choices=[]))
 