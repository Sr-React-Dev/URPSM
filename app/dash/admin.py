from django.contrib import admin
from .models import ContactAdmin
from django.forms import ModelForm#, Textarea, CharField

class ContactAdminFormAdmin(ModelForm):
    # feedback = CharField(required=False, widget=Textarea(
    #     attrs={'class': 'input-text full-width', 'rows':6 , 'placeholder': 'Write feedback here'}))

    class Meta:
        model  = ContactAdmin
        fields = ['user', 'subject', 'type', 'message', 'feedback']

class ContactAdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'message', 'feedback','created_at', 'processed']
    form          = ContactAdminFormAdmin

admin.site.register(ContactAdmin, ContactAdminAdmin)
