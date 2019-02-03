# -*- coding: utf-8 -*-
from __future__ import absolute_import
from django.contrib import admin
from django import forms


from suit_redactor.widgets import RedactorWidget
from suit.widgets import NumberInput, EnclosedInput

from app.dash.models import AdminActionHistory
from .models import Shop, Banner
from .utils import AdminImageWidget
from mobilify import utils
# from app.notifications.models import Notification


# class NotificationsInline(admin.TabularInline):
#     model = Notification


class ShopAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'description': RedactorWidget(editor_options={
                'lang': 'en',
                'buttons': ['html', '|', 'formatting', '|', 'bold', 'italic', '|',
                            'unorderedlist', 'orderedlist', 'outdent', 'indent',
                            'alignment', 'horizontalrule', 'underline'],
                'imageUpload': '/clients/redactor/image/'
            }),
            'balance': NumberInput(attrs={'min': '0'}),
            'balance': EnclosedInput(prepend='$'),
            'location': EnclosedInput(append='icon-map-marker'),
            'vat': EnclosedInput(append='%'),
            'shop_email': EnclosedInput(prepend='icon-envelope'),
            'logo': AdminImageWidget(),
        }


class ShopAdmin(utils.BaseAdmin):
    view_groups = [utils.SHOP_MONITOR_GROUP]
    form = ShopAdminForm
    # inlines = [NotificationsInline]
    search_fields = ['name', 'shop_phone', 'shop_email' ]
    list_filter = ['country', ]
    list_display = (
        'name',
        'shop_phone',
        'shop_email',
        'country', 'city', 'paypal_email',
        'get_balance', 'blocked', 'created')
    fieldsets = [
        (
            None, {
                'fields': ['logo', 'name', 'description', 'balance']
            }
        ),
        (
            'VAT', {
                'fields': ['vat']
            }
        ),
        (
            'Contact information', {
                'fields': ['shop_phone', 'shop_email']
            }
        ),
        (
            'Shop location', {
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
                'fields':['cancellation_charges','completion_charges']
            }
        )

    ]

    def get_balance(self, obj):
        return '<span class="label label-info">$%s</span>' % (obj.balance)

    get_balance.short_description = 'balance'
    get_balance.allow_tags = True

    def get_read_only_fields_for_permissions(self, request, models, readonly_fields):
        if request.user.groups.filter(name=utils.SUBCONTRACTOR_GROUP):
            return ['balance']
        if request.user.groups.filter(name__in=self.view_groups):
            return [f.name for f in models._meta.fields]
        return readonly_fields
    def save_model(self, request, obj, form, change):
        affected = ""
        if change:
            t = "updated"
            affected = ""
            for changed in form.changed_data:
                affected += changed + " updated (New Val:" + str(form.cleaned_data[changed]) + ")."
        else:
            t = "added"
        action = "Shop "+t+" #"+str(obj.id)

        AdminActionHistory.objects.create(action=action,user=request.user,affected=affected)
        super(ShopAdmin, self).save_model(request, obj, form, change)




admin.site.register(Shop, ShopAdmin)


class BannerAdmin(utils.BaseAdmin):
    view_groups = [utils.SHOP_MONITOR_GROUP]
    list_display = ('get_banner', 'link', 'active', 'created',)

    def get_banner(self, obj):
        return '<img src="%s"/>' % obj.banner.thumbnail['400x400]'].url
    get_banner.short_description = 'Thumbnail'
    get_banner.allow_tags = True

admin.site.register(Banner, BannerAdmin)
