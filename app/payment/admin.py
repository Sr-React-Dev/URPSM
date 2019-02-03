from django.contrib import admin
from .models import  ShopPaymentTransaction, ServerPaymentTransaction

# Register your models here.

admin.site.register(ShopPaymentTransaction)
admin.site.register(ServerPaymentTransaction)