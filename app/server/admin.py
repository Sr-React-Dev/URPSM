# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.contrib import admin
from django import forms


from suit_redactor.widgets import RedactorWidget
from suit.widgets import NumberInput, EnclosedInput

from app.dash.models import AdminActionHistory
from .models import Server
from .utils import AdminImageWidget
from mobilify import utils



class ServerAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'description': RedactorWidget(editor_options={
                'lang': 'en',
                'buttons': ['html', '|', 'formatting', '|', 'bold', 'italic', '|',
                            'unorderedlist', 'orderedlist', 'outdent', 'indent',
                            'alignment', 'horizontalrule', 'underline'],
                'imageUpload': '/clients/redactor/image/'
            }),
            'credit': NumberInput(attrs={'min': '0'}),
            'credit': EnclosedInput(prepend='$'),
            'location': EnclosedInput(append='icon-map-marker'),
            'vat': EnclosedInput(append='%'),
            'email': EnclosedInput(prepend='icon-envelope'),
            'logo': AdminImageWidget(),
        }


class ServerAdmin(utils.BaseAdmin):
    view_groups = [utils.SERVER_MONITOR_GROUP]
    form = ServerAdminForm
    search_fields = ['name', 'server_phone', 'server_email', ]
    list_filter = ['country', ]
    list_display = (
        'name',
        'server_phone',
        'server_email',
        'country', 'city', 'paypal_email',
        'get_credit', 'blocked', 'created')
    fieldsets = [
        (
            None, {
                'fields': ['logo', 'name', 'description', 'credit']
            }
        ),
        (
            'VAT', {
                'fields': ['vat']
            }
        ),
        (
            'Contact information', {
                'fields': ['server_phone', 'server_email']
            }
        ),
        (
            'Server location', {
                'fields': ['country', 'city', 'address', 'location']
            }
        ),
        (
            'Links', {
                'fields': ['website', 'facebook', 'twitter', 'google_plus',
                           'paypal_email']
            }
        ),
        (
            'Status', {
                'fields': ['blocked']
            }
        ),
        (
            'Custom charges',{
                'fields':['completion_charges']
            }
        ),
        (
            'Max Allowed APIs', {
                'fields': ['max_allowed_apis']
            }
        )

    ]

    def get_credit(self, obj):
        return '<span class="label label-info">$%s</span>' % (obj.credit)

    def save_model(self, request, obj, form, change):
        affected = ""
        if change:
            t = "updated"
            for changed in form.changed_data:
                affected += changed + " updated (New Val:" + str(form.cleaned_data[changed]) + ")."
        else:
            t = "added"
        action = "Server "+t+" #"+str(obj.id)
        AdminActionHistory.objects.create(action=action,user=request.user,affected=affected)
        super(ServerAdmin, self).save_model(request, obj, form, change)

    get_credit.short_description = 'balance'
    get_credit.allow_tags = True

admin.site.register(Server, ServerAdmin)


# class ServerBannerAdmin(admin.ModelAdmin):
#     list_display = ('get_banner', 'link', 'active', 'created',)

#     def get_banner(self, obj):
#         return '<img src="%s"/>' % obj.banner['small'].url
#     get_banner.short_description = 'Thumbnail'
#     get_banner.allow_tags = True
# admin.site.register(Banner, ServerBannerAdmin)
