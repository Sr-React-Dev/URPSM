from __future__ import absolute_import
import json
from django.contrib import admin
from django import forms
from .models import Endpoint
# from django_select2.widgets import Select2Widget
from mobilify import utils


class EndpointForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EndpointForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance.pk:
            c = instance.get_client()
            if c.status():
                self.fields['networks'] = forms.ChoiceField(
                    choices=json.loads(c.get_networks_list()),)
            else:
                self.fields['networks'] = forms.ChoiceField(
                    choices=(), required=False)
            try:
                self.fields['service'].help_text = ''
            except:
                pass

    def clean_service(self):
        cleaned_data = self.cleaned_data['service']

        if not cleaned_data and self.cleaned_data['networks'] != "":
            raise forms.ValidationError('Select a service(s)', code='invalid')

        return cleaned_data

    class Meta:
        model = Endpoint
        fields = '__all__'

    class Media:
        js = ('/static/js/admin.js', )


class EndpointAdmin(utils.BaseAdmin):
    view_groups = [utils.ENDPOINT_MONITOR_GROUP]
    form = EndpointForm
    list_display = ('url', 'username',
                    'status', 'get_balance', 'get_email', 'active')

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(EndpointAdmin, self).get_form(request, obj, **kwargs)
    #     services = {}
    #     for service in request.POST.getlist('service'):
    #         s = service.split(':')
    #         services[s[0]] = s[1]

    #     print json.dumps(services)
    #     # form.service = json.dumps(services)
    #     return form

    def get_balance(self, obj):
        if obj.account_info() is False:
            return "???"
        return "${} USD".format(json.loads(obj.account_info())['credit'])

    def get_email(self, obj):
        if obj.account_info() is False:
            return "???"
        return json.loads(obj.account_info())['email']

    get_balance.short_description = 'Credit'
    get_email.short_description = 'Email'

    def status(self, obj):
        if obj.status:
            return '<img src="https://urpsm-assets.s3.amazonaws.com/static/admin/img/icon-yes.gif" alt="{}" />'.format(obj.status)
        else:
            return '<img src="https://urpsm-assets.s3.amazonaws.com/static/admin/img/icon-no.gif" alt="{}" />'.format(obj.status)

    status.allow_tags = True

    # def save_model(self, request, obj, form, change):
    #     services = {}
    #     if request.POST.getlist('service')[0] != '':
    #         for service in request.POST.getlist('service'):
    #             s = service.split(':')
    #             services[s[0]] = s[1]
    #     obj.service = json.dumps(services)
    #     obj.save()


admin.site.register(Endpoint, EndpointAdmin)
