from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from app.launch.models import LaunchRock
from django.forms import ModelForm
from django import forms
from django.views.generic import TemplateView

import datetime

class LaunchRockForm(ModelForm):
    class Meta:
        model = LaunchRock
        exclude = ['sign_date', 'ip', 'http_refer', 'notify_him']

    def clean_email(self):
        try:
            LaunchRock.objects.get(email=self.cleaned_data['email'])
        except LaunchRock.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError("This is email is already in database.")


def notify_him(request):
    pass

def signup(request):
    print request.POST
    print request.GET
    if request.method == 'POST':
        print 'POST'
        # if request.POST.get('email'):
        # if request.POST['notify_him'] == "1":
        #     print 1
        #     request.POST['notify_him'] = True
        # else:
        #     print 2
        #     request.POST['notify_him'] = False

        form = LaunchRockForm(data=request.POST)
        if form.is_valid():
            launch = LaunchRock.objects.create(name=form.cleaned_data['username'],notify_him=form.cleaned_data['notify_him'], email=form.cleaned_data['email'],sign_date=datetime.datetime.now(), 
                                ip=request.META['REMOTE_ADDR'], http_refer = request.META['HTTP_REFERER'], message=form.cleaned_data['message'],)
        return HttpResponse(_('Thank you'))
        # else:
            # print "not valid form"
    else:
        form = LaunchRockForm()
    return render_to_response('urpsm/launch/launch.html', { 'form': form }, context_instance=RequestContext(request))

def done(request):
    return render_to_response('urpsm/  launch/done.html')

class TestView(TemplateView):
    template_name = 'urpsm/v2/launch/HTTPCS36990.html'