from __future__ import absolute_import
from random import randint
from django import forms
from django.contrib import admin
#from django.contrib.admin.views.decorators import staff_member_required
from django.template.response import TemplateResponse
from django.conf.urls import patterns, url
from suit_redactor.widgets import RedactorWidget
from suit.widgets import EnclosedInput, SuitSplitDateTimeWidget, NumberInput
from django_select2.widgets import Select2Widget
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from app.dash.models import AdminActionHistory
from .models import Client, Addon, Image
from smart_selects.widgets import ChainedSelect
from mobilify import utils


class SfWidget(Select2Widget, ChainedSelect):
    pass

class AddonAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'price': EnclosedInput(prepend='$'),
            'original_price': EnclosedInput(prepend='$'),
        }


class AddonAdmin(utils.BaseAdmin):
    view_groups = [utils.CLIENT_MONITOR_GROUP]
    form = AddonAdminForm
    list_display = ('type', 'get_price', 'created')

    def get_price(self, obj):
        return '<span class="label label-info">$%s</span>' % (obj.price)

    get_price.short_description = 'price'
    get_price.allow_tags = True


class AddonInline(admin.TabularInline):
    model = Addon
    form = AddonAdminForm
    suit_classes = 'suit-tab suit-tab-addons'


class ImageInline(admin.TabularInline):
    model = Image
    suit_classes = 'suit-tab suit-tab-images'


class ClientAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        if kwargs.has_key('initial'):
            kwargs['initial'] = {}
            kwargs['initial'].update({'ref': u"{}-{}".format(self.current_user.profile.shop.country, randint(1, 999999999))})
        super(ClientAdminForm, self).__init__(*args, **kwargs)

    '''
    def save_model(self, request, obj, form, change):
        if change:
            t = "updated"
        else:
            t = "added"
        action = "Paypal IPN "+t+" #"+str(obj.pk)
        AdminActionHistory.objects.create(action=action,user=request.user,affected="")
        super(ClientAdminForm, self).save_model(request, obj, form, change)
    '''
    def clean_imei(self):
        if len(self.cleaned_data.get('imei')) != 15:
            raise ValidationError(u'Invalid IMEI', code='invalid')

        return self.cleaned_data.get('imei')

    class Meta:
        widgets = {
            'status_description': RedactorWidget(editor_options={
                'lang': 'en',
                'buttons': ['html', '|', 'formatting', '|', 'bold', 'italic', '|',
                            'unorderedlist', 'orderedlist', 'outdent', 'indent',
                            'alignment', 'horizontalrule', 'underline', '|', 'image', '|'],
                'imageUpload': '/clients/redactor/image/',
                'toolbarOverflow': True,
            }),
            'todo_description': RedactorWidget(editor_options={
                'lang': 'en',
                'buttons': ['html', '|', 'formatting', '|', 'bold', 'italic', '|',
                            'unorderedlist', 'orderedlist', 'outdent', 'indent',
                            'alignment', 'horizontalrule', 'underline', '|', 'image', '|'],
                'imageUpload': '/clients/redactor/image/',
                'toolbarOverflow': True,
            }),
            'amount': NumberInput(attrs={'min': '0'}),
            'amount': EnclosedInput(prepend='$'),
            'email': EnclosedInput(prepend='icon-envelope'),
            'delivered_at': SuitSplitDateTimeWidget,
            'brand': Select2Widget(select2_options={
                'width': '220px'
            }),
            'model': SfWidget(
                app_name='phone',
                model_name='model',
                chain_field='brand',
                model_field='brand',
                show_all=False,
                auto_choose=False,
                attrs={'class': 'form-control'},
                select2_options={"width": "220px"}
            ),
        }
    class Media:
        css = {
            'all': ('/static/django_select2/css/select2.min.css', )
        }

        js = (
                '/static/django_select2/js/select2.min.js',
                # '/static/js/admin.js',
            )


class ClientAdmin(utils.BaseAdmin):
    view_groups = [utils.CLIENT_MONITOR_GROUP]
    form = ClientAdminForm
    inlines = [AddonInline, ImageInline]
    search_fields = ['ref',  'phone_number', 'brand__name', 'model__name', 'shop__name', 'paid_for__username']
    list_display = (
        'shop', 'ref', 'brand', 'model', 'phone_number', 'status', 'todo', 'paid', 'paid_for',
        'get_amount', 'delivered_at')

    list_filter = ['paid']

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-phone', ),
            'fields': ['shop', 'ref', 'brand', 'model', 'serial', 'imei', 'phone_number',
                       'email', 'amount', 'status', 'status_description',
                       'todo', 'todo_description', 'paid', 'paid_for', 'delivered_at']
        }),
    ]

    def save_model(self, request, obj, form, change):
        affected = ""
        if change:
            t = "updated"
            for changed in form.changed_data:
                affected += changed + " updated (New Val:" + str(form.cleaned_data[changed]) + ")."
        else:
            t = "added"
        action = "Client "+t+" #"+str(obj.pk)
        AdminActionHistory.objects.create(action=action,user=request.user,affected=affected)
        super(ClientAdmin, self).save_model(request, obj, form, change)

    suit_form_tabs = (
        ('phone', 'Client'), ('addons', 'Addons'), ('images', 'Images'))

    def get_form(self, request, obj=None, **kwargs):
        form = super(ClientAdmin, self).get_form(request, obj, **kwargs)
        form.current_user = request.user
        return form

    def get_urls(self):
        urls = super(ClientAdmin, self).get_urls()
        ticket_urls = patterns('',
                               url(r'^(?P<id>\d+)/ticket/$',
                                   self.admin_site.admin_view(self.ticket))
                               )
        return ticket_urls + urls

    def ticket(self, request, id):
        entry = get_object_or_404(Client, pk=id)
        context = dict(
            self.admin_site.each_context(request),
            obj=entry,
        )
        return TemplateResponse(request, 'admin/client/client/ticket.html', context)

    def get_amount(self, obj):
        return '<span class="label label-info">$%s</span>' % (obj.total)

    get_amount.short_description = 'Amount'
    get_amount.allow_tags = True


class ImageAdmin(utils.BaseAdmin):
    view_groups = [utils.CLIENT_MONITOR_GROUP]
    pass

admin.site.register(Client, ClientAdmin)
admin.site.register(Addon, AddonAdmin)
admin.site.register(Image, ImageAdmin)
