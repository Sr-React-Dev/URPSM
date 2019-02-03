from django.contrib import admin
from app.public.models import Contact
from django.forms import ModelForm, Textarea, CharField


class ContactFormAdmin(ModelForm):
    feedback = CharField(required=False, widget=Textarea(
        attrs={'class': 'input-text full-width', 'rows':6 , 'placeholder': 'Write feedback here'}))

    class Meta:
        model  = Contact
        fields = ['subject', 'name', 'email', 'message', 'feedback']

class ContactAdmin(admin.ModelAdmin):
    form          = ContactFormAdmin
    model         = Contact
    
    list_display  = [ 'subject', "name", 'email', 'created_at', 'processed']


admin.site.register(Contact, ContactAdmin)
