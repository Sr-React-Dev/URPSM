from __future__ import absolute_import
from django import forms

from smart_selects.widgets import ChainedSelect
from django_select2.widgets import Select2Widget
from .models import Component

class SfWidget(Select2Widget, ChainedSelect):
    pass


class CreateComponentForm(forms.ModelForm):

    class Meta:
        model = Component
        exclude = ('sold', 'deleted', 'shop', )
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'brand': forms.Select(
                # attrs={'class': 'form-control'}
                ),
            # 'brand': Select2Widget(select2_options={'width': '100%'}),
            'model': ChainedSelect(
                app_name='phone',
                model_name='model',
                chain_field='brand',
                model_field='brand',
                show_all=False,
                auto_choose=False, 
                # attrs={'class': 'form-control'},
                # select2_options={'width': '100%'}
            ),
            'type': forms.Select(
                # attrs={'class': 'form-control'}
                ),
            # 'type': Select2Widget(select2_options={'width': '100%'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'currency': forms.Select(attrs={'class': 'form-control',}),

        }


class UpdateComponentForm(forms.ModelForm):

    class Meta:
        model = Component
        exclude = ('deleted', 'shop')
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'brand': Select2Widget(select2_options={'width': '100%'}),
            'model': SfWidget(
                app_name='phone',
                model_name='model',
                chain_field='brand',
                model_field='brand',
                show_all=False,
                auto_choose=False, 
                # attrs={'class': 'form-control'},
                select2_options={'width': '100%'}

            ),
            'type': Select2Widget(select2_options={'width': '100%'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'currency': forms.Select(attrs={'class': 'form-control',}),
            

        }
