from __future__ import absolute_import, unicode_literals
from django import forms
# from phonenumber_field.formfields import PhoneNumberField
# from django_countries.data import COUNTRIES
from location_field.widgets import LocationWidget
# from suit_redactor.widgets import RedactorWidget
from .models import Shop
from .utils import FrontImageWidget
from smart_selects.widgets import ChainedSelect
# countries = tuple(sorted(COUNTRIES.items()))
from django import forms
# from haystack.forms import SearchForm


# class ShopComponentSearchForm(SearchForm):
#     component = forms.CharField(required=False widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': ''})
#     end_date = forms.DateField(required=False)

#     def search(self):
#         # First, store the SearchQuerySet received from other processing.
#         sqs = super(DateRangeSearchForm, self).search()

#         if not self.is_valid():
#             return self.no_query_found()

#         # Check to see if a start_date was chosen.
#         if self.cleaned_data['start_date']:
#             sqs = sqs.filter(pub_date__gte=self.cleaned_data['start_date'])

#         # Check to see if an end_date was chosen.
#         if self.cleaned_data['end_date']:
#             sqs = sqs.filter(pub_date__lte=self.cleaned_data['end_date'])

#         return sqs

from django.contrib.auth.models import User


class RegisterShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['name', 'shop_phone', 'shop_email', 'city', 'country']


class ShopCreationForm(forms.ModelForm):

    # def __init__(self, id, *args, **kwargs):
    #     print 'ShopCreationForm', id
    #     super(ShopCreationForm, self).__init__(*args, **kwargs)
    #     self.user = User.objects.filter( pk = id )

    class Meta:
        model = Shop
        exclude = ('balance','rank', 'level')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop name'}),
            'shop_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+212612345678'}),
            'shop_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'foo@example.com'}),
            'vat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '20'}),
            'country': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            # 'city': forms.Select(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'city': ChainedSelect(
                app_name='simplecities',
                model_name='city',
                chain_field='country',
                model_field='country',
                show_all=False,
                auto_choose=False,
                attrs={'class': 'form-control'},
                # select2_options={'width': '100%'}
            ),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop address'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': LocationWidget(attrs={'class': 'form-control'}),
            'logo': FrontImageWidget(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Twitter'}),
            'google_plus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Google Plus'}),
            'paypal_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your paypal account email'}),
        }

        # def save(self, commit=True):
        #     shop = super(ShopCreationForm, self).save(commit=True)
        #     return shop
            






class ShopUpdateForm(forms.ModelForm):

    class Meta:
        model = Shop
        exclude = ('balance', 'rank','level')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop name'}),
            'shop_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+212612345678'}),
            'shop_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'foo@example.com'}),
            'vat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '20'}),
            'country': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Country'}),
            # 'city': forms.Select(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'city': ChainedSelect(
                app_name='simplecities',
                model_name='city',
                chain_field='country',
                model_field='country',
                show_all=False,
                auto_choose=False,
                attrs={'class': 'form-control'},
                # select2_options={'width': '100%'}
            ),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Shop address'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': LocationWidget(attrs={'class': 'form-control'}),
            'logo': FrontImageWidget(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Website'}),
            'facebook': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Facebook'}),
            'twitter': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Twitter'}),
            'google_plus': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Google Plus'}),
            'paypal_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your paypal account email'}),
        }


class ShopContact(forms.Form):
    shop = forms.CharField(widget=forms.HiddenInput())
    component = forms.CharField(widget=forms.HiddenInput())
    message = forms.CharField(required=True, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Message'}))



from app.search.forms import SearchForm

class ShopEndpointNetworkSearchForm(SearchForm):
    def search():
        backend = get_search_backend('default')
        query = self.cleaned_data['q']