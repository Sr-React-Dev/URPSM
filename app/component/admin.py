from __future__ import absolute_import
from django import forms
from django.contrib import admin
from django.utils.html import mark_safe

from suit_redactor.widgets import RedactorWidget
from suit.widgets import NumberInput, EnclosedInput
from django_select2.widgets import Select2Widget

# from easy_thumbnails.files import get_thumbnailer
from app.dash.models import AdminActionHistory
from .models import Type, Component
from smart_selects.widgets import ChainedSelect
from mobilify import utils


class SfWidget(Select2Widget, ChainedSelect):
    pass


class AdminImageWidget(forms.FileInput):

    """A ImageField Widget for admin that shows a thumbnail."""

    def __init__(self, attrs={}):   # pylint: disable=E1002,W0102
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):  # pylint: disable=E1002
        output = []
        css = {'style': 'clear:left;float:left;margin:1em 1em 0 0;'}
        output.append(super(AdminImageWidget, self).render(name, value,
                                                           attrs=css))
        if value and hasattr(value, "url"):
            output.append(('<a target="_blank" href="%s">'
                           '<img class="img-polaroid" src="%s" alt="" '
                           'style="float:right;width:128px;height:128px;" /></a>'
                           % (value.url, value.url)))
        return mark_safe(u''.join(output))


class ComponentAdminForm(forms.ModelForm):

    class Meta:
        widgets = {
            'image': AdminImageWidget(),
            'description': RedactorWidget(editor_options={
                'lang': 'en',
                'buttons': ['html', '|', 'formatting', '|', 'bold', 'italic', '|',
                            'unorderedlist', 'orderedlist', 'outdent', 'indent',
                            'alignment', 'horizontalrule', 'underline', '|', 'image', '|', 'link'],
                'imageUpload': '/clients/redactor/image/',
            }),
            'price': NumberInput(attrs={'min': '0'}),
            'price': EnclosedInput(prepend='$'),
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
            'type': Select2Widget(select2_options={
                'width': '220px'
            }),
        }

    class Media:
        css = {
            'all': ('/static/django_select2/css/select2.min.css', )
        }

        js = (
            '/static/django_select2/js/select2.min.js',
            # '/static/js/admin.js',
        )


class ComponentAdmin(utils.BaseAdmin):
    view_groups = [utils.COMPONENT_MONITOR_GROUP]
    form = ComponentAdminForm
    list_display = ('get_image', 'title', 'shop', 'brand', 'model', 'type',
                    'price', 'sold', 'deleted', 'created')
    list_filter = ['sold', 'deleted']
    list_display_links = ('shop', )
    search_fields = ['title', 'shop__name',
                     'brand__name', 'model__name', 'type__name', ]

    def get_image(self, obj):
        return '<img src="%s"/>' % obj.image.thumbnail['32x32'].url
    get_image.short_description = 'Thumbnail'
    get_image.allow_tags = True

    def save_model(self, request, obj, form, change):
        affected = ""
        if change:
            t = "updated"
            for changed in form.changed_data:
                affected += changed + " updated (New Val:" + str(form.cleaned_data[changed]) + ")."
        else:
            t = "added"
        action = "Component "+t+" #"+str(obj.id)
        AdminActionHistory.objects.create(action=action,user=request.user,affected=affected)
        super(ComponentAdmin, self).save_model(request, obj, form, change)


class BrandAdmin(utils.BaseAdmin):
    view_groups = [utils.COMPONENT_MONITOR_GROUP]
    # exclude = ('slug', )
    pass


class ModelAdmin(utils.BaseAdmin):
    # exclude = ('slug', )
    view_groups = [utils.COMPONENT_MONITOR_GROUP]
    pass


class TypeAdmin(utils.BaseAdmin):
    # exclude = ('slug', )
    view_groups = [utils.COMPONENT_MONITOR_GROUP]
    pass

admin.site.register(Component, ComponentAdmin)
# admin.site.register(Brand, BrandAdmin)
# admin.site.register(Model, ModelAdmin)
admin.site.register(Type, TypeAdmin)
