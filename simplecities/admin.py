from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


from .models import Country, City


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']

class CityAdmin(admin.ModelAdmin):
    list_display = ['name','country']



admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
