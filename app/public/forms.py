from django import forms
from django.utils.translation import activate, ugettext_lazy as _
from .models import Contact 
from app.phone.models import Brand, Model
from smart_selects.widgets import ChainedSelect


class ContactForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'input-text full-width', 'placeholder': _('name')}))
    subject = forms.CharField(required=True, widget=forms.TextInput(
        attrs={'class': 'input-text full-width', 'placeholder': _('subject')}))

    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={'class': 'input-text full-width', 'placeholder': _('email')}))
    website = forms.URLField(required=False, widget=forms.URLInput(
        attrs={'class': 'input-text full-width', 'placeholder': _('website')}))

    message = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'input-text full-width', 'rows':6 , 'placeholder': _('Write message here')}))

    class Meta:
        model = Contact
        exclude = ('created_at', )

class BrandSearchForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all().order_by('name'))
    model = forms.ChoiceField()

    class Meta:
        widgets = {
            'model': ChainedSelect(
                app_name='phone',
                model_name='model',
                chain_field='id_brand',
                model_field='brand',
                show_all=False,
                auto_choose=False,
                attrs={'class': 'form-control'},
                # select2_options={"width": "100%"}
            ),
        }

# class AdminContact(forms.Model):
#     subject = forms.CharField(required=True, widget=forms.TextInput(
#         attrs={'class': 'input-text full-width', 'placeholder': _('subject')}))
#     type    = forms.CharField(required=True, widget=forms.Select(choices=( ('administrative', _('administrative') ), ('technical', _('technical') ),) , attrs={'class': 'input-text full-width', 'placeholder': _('type')})))

#     message = forms.CharField(required=True, widget=forms.Textarea(
#         attrs={'class': 'input-text full-width', 'rows':6 , 'placeholder': _('Write message here')}))

    # class Meta:
    #     model = Contact
    #     exclude = ('created_at', )
    

# class ContactForm(forms.Form):
#     name = forms.CharField(required=True, widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Name'}))
#     email = forms.EmailField(required=True, widget=forms.EmailInput(
#         attrs={'class': 'form-control', 'placeholder': 'Email'}))

#     message = forms.CharField(required=True, widget=forms.Textarea(
#         attrs={'class': 'form-control', 'placeholder': 'Message'}))
#     