from __future__ import absolute_import
from django.contrib import admin
from django import forms
# from django_select2.widgets import Select2Widget
from .models import Brand, Model
# , Picture
from app.shop.utils import AdminImageWidget
from mobilify import utils



class ModelFormAdmin(forms.ModelForm):

    class Meta:
        widgets = {
            # 'brand': Select2Widget(select2_options={
            #     'width': '220px'
            # }),
        }


class ModelInline(admin.TabularInline):
    model = Model
    # extra = 3
    class Meta:
        fields = ['name', 'picture']


# class ImageInline(admin.StackedInline):
# 	model = Picture
# 	extra = 1

class ModelAdmin(utils.BaseAdmin):
    view_groups = [utils.PHONE_MONITOR_GROUP]
    '''
        Admin View for Model
    '''
    form = ModelFormAdmin
    list_display = ('name', 'brand')
    search_fields = ['name','brand__name']
    # inlines = [ImageInline]

    def get_readonly_fields(self, request, obj=None):
        try:
            return utils.get_read_only_fields_for_permissions(request, self.model, self.readonly_fields)
        except:
            return []


# class PictureAdmin(admin.ModelAdmin):
#     list_display = ('model', 'brand', )
#     list_filter = ('brand', )

class BrandFormAdmin(forms.ModelForm):

    class Meta:
        widgets = {
            'logo': AdminImageWidget(),
        }


class BrandAdmin(utils.BaseAdmin):
    view_groups = [utils.PHONE_MONITOR_GROUP]
    form = BrandFormAdmin
    inlines = [ModelInline]
    list_display = ('get_image', 'name', )

    def get_image(self, obj):
        img_url = obj.logo.crop['120x120'].url if obj.logo else '/static/images/crossword.png'
        return '<img src="%s" height="24" width="32"/>' % img_url
    get_image.short_description = 'Thumbnail'
    get_image.allow_tags = True


admin.site.register(Brand, BrandAdmin)
admin.site.register(Model, ModelAdmin)
# admin.site.register(Picture, PictureAdmin)
