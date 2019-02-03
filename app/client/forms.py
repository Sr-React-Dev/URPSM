from __future__ import absolute_import
from django import forms
from django.forms.models import inlineformset_factory
from django.core.exceptions import ValidationError
# from suit.widgets import SuitTimeWidget, SuitSplitDateTimeWidget
from smart_selects.widgets import ChainedSelect
# from django_select2.widgets import Select2Widget
from .models import Client, Image, Addon
from braces.forms import UserKwargModelFormMixin


# class SfWidget(Select2Widget, ChainedSelect):
#     pass


class CreateClientForm(UserKwargModelFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateClientForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.pk:
            if self.user and hasattr(self.user, 'profile'):
                if instance.paid:
                    for key in self.fields.keys():
                        # if key != 'todo' and key != 'status' and key != 'status_description' and key != 'todo_description':
                            self.fields[key].widget.attrs['readonly'] = "true"
                            self.fields[key].widget.attrs['disabled'] = "true"

    def clean_imei(self):
        if len(self.cleaned_data.get('imei')) != 15:
            raise ValidationError(u'Invalid IMEI', code='invalid')

        return self.cleaned_data.get('imei')

    class Meta:
        model = Client
        exclude = ('shop', 'paid_for', 'deleted', 'delivered_at')
        widgets = {
            'brand': forms.Select(
                # attrs={'class': 'form-control'}
            ),
            # 'brand': Select2Widget(select2_options={'width': '100%'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'todo': forms.Select(attrs={'class': 'form-control'}),
            'model': ChainedSelect(
                app_name='phone',
                model_name='model',
                chain_field='brand',
                model_field='brand',
                show_all=False,
                auto_choose=False,
                # attrs={'class': 'form-control'},
                # select2_options={"width": "100%"}
            ),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'placeholder': 'Amount'}),
            'status_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Status description'}),
            'todo_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Todo description'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial'}),
            'imei': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Imei'}),
            'ref': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ref', 'readonly': 'true'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'serial': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serial'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+212612345678'}),
            'delivery_time': forms.DateTimeInput(attrs={'class': 'form-control'}),

        }


class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ('image', 'client')

        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }


class AddonForm(forms.ModelForm):

    class Meta:
        model = Addon
        fields = ('type', 'name', 'price', 'original_price', 'client')

        widgets = {
            'type': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Type'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'original_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Original Price'})
        }

ImageFormSet = inlineformset_factory(Client, Image, form=ImageForm, extra=1,)
AddonFormSet = inlineformset_factory(Client, Addon, form=AddonForm, extra=1,)


class FilterForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('status', 'todo', 'paid')
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Type'}),
            'todo': forms.Select(attrs={'class': 'form-control', }),
            # 'paid': forms.NumberInput(attrs={'class': 'form-control', })
        }
