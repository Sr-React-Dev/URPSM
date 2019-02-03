from __future__ import absolute_import
import json
import os
from random import randint
from django.conf import settings
from django.core import serializers
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, TemplateView, View, DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404
from django.db.models import Q
from django.utils import timezone

# from django.core.exceptions import ValidationError
from app.shop.models import ActionHistory

try:
    import magic
except:
    pass
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from .forms import CreateClientForm, AddonFormSet, ImageFormSet, FilterForm
from .models import Client
from app.phone.models import Model
from app.ureview.views import ShopReview
from app.account.views import HasBusinessMixin


@csrf_exempt
@require_POST
@login_required
def redactor_image(request):
    allowed_ext = ['png', 'jpg', 'jpeg']
    allowed_mimes = ['image/png', 'image/jpeg']
    mimetype = magic.from_buffer(request.FILES['file'].read(), mime=True)
    ext = (request.FILES['file'].name).split('.')[-1]
    if mimetype in allowed_mimes and ext in allowed_ext:
        dest = os.path.join(
            settings.MEDIA_ROOT, request.FILES['file']._get_name())
        with open(dest, 'wb') as destination:
            for chunk in request.FILES['file'].chunks():
                destination.write(chunk)
            destination.close()
        link = settings.MEDIA_URL + request.FILES['file']._get_name()
        images = []
        images.append({'filelink': link})

        return HttpResponse(json.dumps(images))

    return HttpResponse(json.dumps({'error': True}))


class CreateClientView(LoginRequiredMixin,CreateView):
    template_name = 'urpsm/clients/create.html'
    form_class = CreateClientForm

    def get_initial(self):
        try:
            return {'ref': u"{}-{}".format(self.request.user.profile.shop.country, randint(1, 999999999))}
        except:
            return {'ref': u"{}-{}".format(self.request.user.profile.server.country, randint(1, 999999999))}

    def get_context_data(self, **kwargs):
        context = super(CreateClientView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['addonformset'] = AddonFormSet(self.request.POST)
            context['imageformset'] = ImageFormSet(
                self.request.POST, self.request.FILES)
        else:
            context['addonformset'] = AddonFormSet()
            context['imageformset'] = ImageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        addonformset = context['addonformset']
        imageformset = context['imageformset']
        # client = form.save(commit=False)
        # client.shop = self.request.user.profile.shop

        # if client.paid:
        #     client.paid_for = self.request.user

        # instance = client.save()

        form.instance.shop = self.request.user.profile.shop
        if form.instance.todo == 'r':
            form.instance.model.repairing_request = form.instance.model.repairing_request + 1
        if form.instance.todo == 'u':
            form.instance.model.unlocking_request = form.instance.model.unlocking_request + 1
        if form.instance.todo == 'f':
            form.instance.model.flashing_request = form.instance.model.flashing_request + 1

        if form.instance.paid:
            form.instance.paid_for = self.request.user
            if form.instance.status =='r':
                if form.instance.todo == 'r':
                    form.instance.model.repaired_items = form.instance.model.repaired_items + 1
                if form.instance.todo == 'u':
                    form.instance.model.unlocked_items = form.instance.model.unlocked_items + 1
                if form.instance.todo == 'f':
                    form.instance.model.flashed_items = form.instance.model.flashed_items + 1

        form.instance.model.save()

        self.object = form.save()
        try:
            ActionHistory.objects.create(shop=self.request.user.profile.shop, action="New client added #" + self.object.id,
                                     user=self.request.user)
        except Exception:
            pass


        if addonformset.is_valid():
            print "addon formset is valid"
            addonformset.instance = self.object
            addonformset.save()
        if imageformset.is_valid():
            print "image formset is valid"
            imageformset.instance = self.object
            imageformset.save()
        return super(CreateClientView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('clients')


class ClientsView(LoginRequiredMixin,ListView):
    template_name = 'urpsm/clients/index.html'
    model = Client
    paginate_by = 15
    context_object_name = 'clients'

    def get_queryset(self):
        return Client.objects.select_related().filter(shop=self.request.user.profile.shop, deleted=False).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(ClientsView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        term = ''
        if 'q' in request.GET and request.GET.get('q').strip():
            term = request.GET.get('q').strip()
            self.object_list = self.get_queryset().filter(Q(ref__icontains=term))

        # status
        if 'status' in request.GET and request.GET.get('status').strip() and 'todo' in request.GET and request.GET.get('todo').strip():
            status = request.GET.get('status').strip()
            todo = request.GET.get('todo').strip()
            if 'paid' in request.GET and request.GET.get('paid').strip():
                paid = request.GET.get('paid').strip()
                self.object_list = self.get_queryset().filter(
                    paid=paid, status=status, todo=todo)
            else:
                self.object_list = self.get_queryset().filter(status=status, todo=todo)

        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if (self.get_paginate_by(self.object_list) is not None
                    and hasattr(self.object_list, 'exists')):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404("Empty list and '%(class_name)s.allow_empty' is False."
                              % {'class_name': self.__class__.__name__})
        context = self.get_context_data()
        context['filter_form'] = FilterForm()
        return self.render_to_response(context)


class QRTicketView(LoginRequiredMixin,  TemplateView):
    template_name = 'urpsm/clients/ticket.html'

    def get(self, *args,  **kwargs):    
        if ShopReview.objects.filter(shop=self.get_object().shop, client=self.get_object()).exists():
          return  redirect(reverse_lazy('error-404'))
        else:
          return super(QRTicketView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QRTicketView, self).get_context_data(**kwargs)
        context['obj'] = self.get_object()
        context['scheme'] = self.request.scheme
        context['host'] = self.request.get_host()
        return context
    def get_object(self, query_set=None):
        return get_object_or_404(Client, shop=self.request.user.profile.shop, pk=self.kwargs.get('pk', None))


class UpdateClientView(LoginRequiredMixin, UpdateView):
    model = Client
    template_name = 'urpsm/clients/update.html'
    form_class = CreateClientForm

    def get_form_kwargs(self):
        kwargs = super(UpdateView, self).get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
            kwargs.update({'user': self.request.user})
        return kwargs

    def get_object(self, queryset=None):
        return get_object_or_404(Client,
                                 pk=self.kwargs.get(self.pk_url_kwarg, None), shop=self.request.user.profile.shop)

    def form_valid(self, form):
        context = self.get_context_data()
        addonformset = context['addonformset']
        imageformset = context['imageformset']
        form.instance.shop = self.request.user.profile.shop

        if form.instance.paid:
            form.instance.paid_for = self.request.user
            if not form.instance.status =='r':
                if form.instance.todo == 'r':
                    form.instance.model.repaired_items = form.instance.model.repaired_items + 1
                if form.instance.todo == 'u':
                    form.instance.model.unlocked_items = form.instance.model.unlocked_items + 1
                if form.instance.todo == 'f':
                    form.instance.model.flashed_items = form.instance.model.flashed_items + 1
                form.instance.status="r"
                form.instance.model.save()



        self.object = form.save()
        try:
            ActionHistory.objects.create(shop=self.request.user.profile.shop, action="Client updated #" + self.object.id,
                                     user=self.request.user)
        except Exception:
            pass
        users = User.objects.filter(profile__shop=self.object.shop)
        if self.object.status=='r':
            for user in users:
                user.profile.notify_client_status_changed(self.object.shop, self.object, self.request.user )
        if self.object.paid:
            for user in users:
                user.profile.notify_client_paid_for_at(self.object.shop, self.object, self.request.user )


        if addonformset.is_valid():
            addonformset.instance = self.object
            addonformset.save()
        if imageformset.is_valid():
            imageformset.instance = self.object
            imageformset.save()

        return super(UpdateClientView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(UpdateClientView, self).get_context_data(**kwargs)

        if self.request.POST:
            if not self.object.paid:
                context['addonformset'] = AddonFormSet(
                    self.request.POST, instance=self.get_object())
                context['imageformset'] = ImageFormSet(
                    self.request.POST, self.request.FILES, instance=self.get_object())
            else:
                context['addonformset'] = AddonFormSet(instance=self.get_object())
                context['imageformset'] = ImageFormSet(instance=self.get_object())
            # addon = AddonFormSet(instance=self.get_object())
            # import pprint
            # pprint.pprint(addon.can_delete)
        return context

    def get_success_url(self):
        return reverse_lazy('clients')


class DeleteClientView(LoginRequiredMixin,GroupRequiredMixin, View):
    group_required = u'Administrator'

    def get(self, *args, **kwargs):
        client = get_object_or_404(
            Client, pk=self.kwargs.get('pk', None), shop=self.request.user.profile.shop)

        client.deleted = True
        client.save()
        try:
            ActionHistory.objects.create(shop=self.request.user.profile.shop, action="Client deleted #" + client.id,
                                     user=self.request.user)
        except Exception:
            pass
        return redirect(reverse_lazy('clients'))


class PaidClientView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        pk=self.request.GET.get('pk', None)
        if pk:
            pk= int(pk)
            client = get_object_or_404(
                Client, pk=pk, shop=self.request.user.profile.shop)
            print client
            client.paid = True
            client.paid_for = self.request.user
            client.status='r'
            client.save()
            return HttpResponse(json.dumps({'status':True}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({'status':False}), content_type="application/json")
        # return redirect(reverse_lazy('clients'))
        


class DetailClientView(LoginRequiredMixin,View):

    def get(self, *args, **kwargs):
        client = get_object_or_404(
            Client, pk=self.request.GET.get('pk', None), shop=self.request.user.profile.shop)
        client = serializers.serialize('json', [client, ])
        return JsonResponse({'client': json.dumps(client)})


class ClientReviewView(DetailView):
    template_name = 'urpsm/v2/client/review_v2.html'
    model = Client
    context_object_name = 'client'

    def get(self, *args,  **kwargs):    
        if ShopReview.objects.filter(shop=self.get_object().shop, client=self.get_object()).exists():
          return  redirect(reverse_lazy('error-404'))
        else:
          return super(ClientReviewView, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientReviewView, self).get_context_data(**kwargs)
        now = timezone.now()
        # x = self.object.delivery_time - now
        # print x
        try:
            if self.object.delivery_time >= now:
                context['delivery_time_exceeded'] = False
            else:
                context['delivery_time_exceeded'] = True
        except:
            if self.object.delivered_at >= now:
                context['delivery_time_exceeded'] = False
            else:
                context['delivery_time_exceeded'] = True


        return context

    def get_object(self, query_set=None):
        return get_object_or_404(Client, uuid=self.kwargs.get('uuid', None))
