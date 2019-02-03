from django import forms
from django.utils.translation import activate,ungettext_lazy, ugettext as _
from .models import ContactAdmin, CHOICES
from django.utils.translation import ugettext_lazy as _


class ContactAdminForm(forms.ModelForm):
    subject = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': _('subject')}))
    type = forms.CharField(required=True, widget=forms.Select(
        attrs={'class': 'form-control', 'placeholder': _('type')}, choices=CHOICES))

    message = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'rows':6 , 'placeholder': _('Write message here')}))

    class Meta:
        model = ContactAdmin
        exclude = ('created_at', )