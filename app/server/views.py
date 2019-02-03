# -*- coding: utf-8 -*-
from __future__ import absolute_import
import json
from random import random
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.views.generic.edit import UpdateView
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.core.mail import send_mail
from braces.views import LoginRequiredMixin, GroupRequiredMixin

from app.payment.models import CREDIT, ServerPaymentTransaction
from .forms import ServerUpdateForm, ServerCreationForm
from .models import Server
from app.component.models import Component
from app.server.forms import ServerContact
from app.endpoint.models import Endpoint
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from app.ureview.models import ServerReview, OrderReview
from el_pagination.views import AjaxListView
from app.account.views import HasBusinessMixin
from app.search.backends import get_search_backend
import app.payment.utils as payment_utils

def make_deposite(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        custom = json.loads(ipn_obj.custom)
        server = Server.objects.get(uuid=custom.server_uuid)
        server.balance += Decimal(ipn_obj.mc_gross)
        server.save()

valid_ipn_received.connect(make_deposite)


class UpdateServerView(LoginRequiredMixin,GroupRequiredMixin, UpdateView):
    template_name = 'urpsm/server/update.html'
    form_class = ServerUpdateForm
    success_url = '.'
    group_required = u'Administrator'

    # def post(self, *args, **kwargs):
    #     form_class = self.get_form_class()
    #     form       = form_class(self.request.POST, self.request.FILES)
    #     if form.is_valid():
    #         print form
    #         return form_valid(form)
    #     else:
    #         print self.get_form_kwargs()
    #         return form_invalid(form, **kwargs)
        

    def get_object(self):
        return get_object_or_404(Server, pk=self.request.user.profile.server.pk)


class CreateServerView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    template_name  = 'urpsm/server/update.html'
    form_class     = ServerCreationForm
    group_required = u'Administrator'

    def get(self, request, *args, **kwargs):
        super(CreateServerView, self).get(request, *args, **kwargs)
        if request.user.profile.shop or request.user.profile.server:
            return redirect(reverse_lazy('error-404'))
        form_class      = self.get_form_class()
        form            = self.get_form(form_class)
        context         = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form       = self.form_class(self.request.POST, self.request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, **kwargs)

    def form_invalid(self, form, **kwargs):
        context         = self.get_context_data(**kwargs)
        context['form'] = ServerCreationForm(self.request.POST, self.request.FILES)
        print context['form'].errors
        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        # take some other action here
        form.save(commit=True)
        self.request.user.profile.server = form.instance
        self.request.user.profile.has_business = True
        self.request.user.profile.save()
        return redirect(reverse_lazy('server-position'))
    



class ServersListView(LoginRequiredMixin, ListView):
    template_name = 'urpsm/v2/server/server_list_v2.html'
    paginate_by = 5
    model = Server
    context_object_name = 'servers'

    def get_queryset(self):
        return Server.objects.filter(blocked=False)


class ServerDetailView(LoginRequiredMixin, DetailView):
    template_name = 'urpsm/server/detail.html'
    model = Server
    context_object_name = 'server'

    def get_object(self, queryset=None):
            return get_object_or_404(Server, slug=self.kwargs.get('slug'))
            

    def get_context_data(self, **kwargs):
        context = super(ServerDetailView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.object  = self.get_object()
        context      = self.get_context_data()
        # try:
        #     endpoint = Endpoint.objects.get(server=self.object)
        # except Endpoint.DoesNotExist:
        #     endpoint = None
        # if endpoint:
            # context['network'] = endpoint.networks.all()
            # context['service'] = endpoint.service
        # else:
            # context['network'] = None
            # context['service'] = None

        context['city'] = self.object.city
        return self.render_to_response(context)

class ServerPositionView(LoginRequiredMixin, DetailView, AjaxListView):
    template_name       = 'urpsm/v2/server/server_position_v2.html'
    model               = Server
    context_object_name ='server'
    page_template       = "urpsm/v2/server/server_review_box_v2.html"
    object_list         = []

    def get(self, request, *args, **kwargs):
        if not self.request.user.profile.server == self.get_object():
            return redirect(reverse('error-404'))
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['world_rank']   = self.object.rank
        context['country_rank'] = Server.objects.filter(country=self.object.country, rank__lt=self.object.rank).count() + 1
        context['city_rank'] = Server.objects.filter(city=self.object.city, rank__lt=self.object.rank).count() + 1
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super(ServerPositionView, self).get_context_data(**kwargs)
        context['reviews'] = OrderReview.objects.filter(server=self.get_object()).values('pk', 'content', 'rating', 'user__username','language','creation_date',
                'order__service', 'order__imei', 'order__shop__logo').distinct().order_by('-creation_date')
        context['page_template'] =  "urpsm/v2/server/server_review_box_v2.html"
        return context

    def get_object(self, query_set=None):
        return get_object_or_404( Server, pk=self.request.user.profile.server.pk )

class DepositView(LoginRequiredMixin, GroupRequiredMixin, TemplateView):
    template_name = 'urpsm/server/deposit.html'
    group_required = u'Administrator'

    def get_context_data(self, **kwargs):
        context = super(DepositView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "item_name": "name of the item",
            "invoice": random(),
            "notify_url": ("%s://%s%s") % (request.scheme, request.get_host(), reverse('paypal-ipn')),
            "return_url": "http://www.urpsm.com/",
            "cancel_return": "http://www.urpsm.com/",
            "custom": json.dumps({'server_uuid': str(request.user.profile.server.uuid), 'username': request.user.username})
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context['form'] = form
        return self.render_to_response(context)

@login_required
@transaction.atomic
def addServerCredits(request):
    if request.method == 'POST':
        credit = request.POST['credit']
        req_server = request.user.profile.server
        req_server.credit += int(credit)
        req_server.save()
        payment_utils.create_server_payment_transaction(req_server, int(credit), req_server.credit, CREDIT,
                                                     "Credit manually by server")
        return render(request,"urpsm/server/addservercredits.html",{"request":request,"success_msg":"Credits successfully added ","credit":req_server.credit})
    return render(request,"urpsm/server/addservercredits.html",{"credit":request.user.profile.server.credit})

@login_required
def serverCreditHistory(request):
    trans = ServerPaymentTransaction.objects.filter(server=request.user.profile.server)
    return render(request,"urpsm/server/viewservercredithistory.html",{"transcations":trans})

class ServerSearchView(LoginRequiredMixin, HasBusinessMixin, TemplateView, AjaxListView):
    template_name               = 'urpsm/v2/search/server_search_result_v2.html'
    model                       = Endpoint
    context_object_name         = 'endpoint'
    page_template               = "urpsm/v2/search/server_search_result_box_v2.html"
    object_list                 = []
    
    def get(self, request, *args, **kwargs):
        order_criterion         = request.GET.get('order_by', '-server__average_rating')
        query                   = request.GET.get('q', '')
        context                 = self.get_context_data()
        backend                 = get_search_backend('default')
        context['query']        = query
        endpoints               = Endpoint.objects.all().order_by(order_criterion)
        results                 = backend.search(query, model_or_queryset=endpoints, operator="or")
        context['endpoints']    = results
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context                  = super(ServerSearchView, self).get_context_data(**kwargs)
        context['page_template'] = "urpsm/v2/search/server_search_result_box_v2.html"
        context['object_list']   = []
        return context
