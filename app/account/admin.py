# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group

from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.ipn.admin import PayPalIPNAdmin

# from suit_redactor.widgets import RedactorWidget
from app.dash.models import AdminActionHistory
from .models import Profile
from mobilify import utils


class ProfileAdminForm(forms.ModelForm):

    class Meta:
        exclude = (
            'activation_key', 'unconfirmed_email', 'email_confirmation_key', )
        # widgets = {
        #     'address': RedactorWidget(editor_options={'lang': 'en'}),
        # }



class ProfileInline(admin.StackedInline):
    form = ProfileAdminForm
    model = Profile
    can_delete = False
    verbose_name_plural = 'Shop'

    def save_model(self, request, obj, form, change):
        if change:
            t = "updated"
        else:
            t = "added"
        action = "Profile "+t+" #"+str(obj.id)
        AdminActionHistory.objects.create(action=action,user=request.user,affected="")
        super(ProfileInline,self).save_model(request, obj, form, change)



class UserAdmin(UserAdmin, utils.BaseAdmin):
    view_groups = [utils.USER_MONITOR_GROUP]
    inlines = (ProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'blocked', 'shop')

    def save_model(self, request, obj, form, change):
        affected = ""
        if change:
            t = "updated"
            for changed in form.changed_data:
                affected += changed + " updated (New Val:" + str(form.cleaned_data[changed]) + ")."
        else:
            t = "added"
        action = "User "+t+" #"+str(obj.id)
        AdminActionHistory.objects.create(action=action,user=request.user,affected=affected)
        super(UserAdmin, self).save_model(request, obj, form, change)

    def get_fieldsets(self, request, obj=None):
        if request.user.groups.filter(name__in=self.view_groups):
            fieldsets = (
                (None, {'fields': ('username', 'password')}),
                (('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (('Important dates'), {'fields': ('last_login', 'date_joined')})
            )
            return fieldsets
        else:
            return super(UserAdmin, self).get_fieldsets(request, obj=obj)

    def blocked(self, obj):
        if obj.profile.block_access:
            return '<img src="/static/admin/img/icon-yes.gif" alt="{}" />'.format(obj.profile.block_access)
        else:
            return '<img src="/static/admin/img/icon-no.gif" alt="{}" />'.format(obj.profile.block_access)
    blocked.allow_tags = True

    def shop(self, obj):
        return obj.profile.shop


class GroupAdmin(GroupAdmin, utils.BaseAdmin):
    view_groups = [utils.USER_MONITOR_GROUP]

    def save_model(self, request, obj, form, change):
        affected = ""
        if change:
            t = "updated"
            for changed in form.changed_data:
                affected += changed + " updated (New Val:" + str(form.cleaned_data[changed]) + ")."
        else:
            t = "added"
        action = "Profile "+t+" #"+str(obj.pk)
        AdminActionHistory.objects.create(action=action,user=request.user,affected=affected)
        super(GroupAdmin, self).save_model(request, obj, form, change)


class PayPalIPNAdmin(PayPalIPNAdmin, utils.BaseAdmin):
    view_groups = [utils.PAYPAL_IPN_MONITOR_GROUP]

    def save_model(self, request, obj, form, change):
        if change:
            t = "updated"
        else:
            t = "added"
        action = "Paypal IPN "+t+" #"+str(obj.pk)
        AdminActionHistory.objects.create(action=action,user=request.user,affected="")
        super(PayPalIPNAdmin, self).save_model(request, obj, form, change)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(PayPalIPN)
admin.site.register(User, UserAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(PayPalIPN, PayPalIPNAdmin)
