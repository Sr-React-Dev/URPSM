# -*- coding: utf-8 -*-
from __future__ import absolute_import

import base64
import hashlib
import json
import os
import urllib
from random import random
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.views.generic.edit import UpdateView
from django.views.generic import ListView, DetailView, TemplateView, FormView
from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse_lazy,  reverse
from django.conf import settings
from django.core.mail import send_mail
from braces.views import LoginRequiredMixin, GroupRequiredMixin

from app.account.utils import mailer
from app.dash.models import KeyValueStore
from app.notifications.models import Notification
from mobilify.settings import DEFAULT_FROM_EMAIL
from .forms import ShopUpdateForm, ShopCreationForm, ShopEndpointNetworkSearchForm
from .models import Shop, Invoices, SFileUpload, InvoiceCharges, ActionHistory, BitcoinHistory, BitcoinKeyInvoiceDict
from app.component.models import Component
from app.shop.forms import ShopContact
from el_pagination.views import AjaxListView
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from app.account.views import HasBusinessMixin
from blockchain.v2.receive import receive
from blockchain.exchangerates import to_btc

def make_deposite(sender, **kwargs):
    ipn_obj = sender

    if ipn_obj.payment_status == ST_PP_COMPLETED:
        custom = json.loads(ipn_obj.custom)
        shop = Shop.objects.get(uuid=custom.shop_uuid)
        shop.balance += Decimal(ipn_obj.mc_gross)
        shop.save()

valid_ipn_received.connect(make_deposite)


class UpdateShopView(LoginRequiredMixin,GroupRequiredMixin, UpdateView):
    template_name = 'urpsm/shop/update.html'
    form_class = ShopUpdateForm
    success_url = '.'
    group_required = u'Administrator'

    def get_object(self):
        return get_object_or_404(Shop, uuid=self.request.user.profile.shop.uuid)


class CreateShopView(LoginRequiredMixin, GroupRequiredMixin, FormView):
    template_name = 'urpsm/shop/update.html'
    form_class = ShopCreationForm
    # success_url = ''
    group_required = u'Administrator'
    # model         = Shop

    def get(self, request, *args, **kwargs):
        if request.user.profile.shop or request.user.profile.server:
            return redirect(reverse_lazy('error-404'))
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = ShopCreationForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form, **kwargs)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = ShopCreationForm(self.request.POST, self.request.FILES)
        print context['form'].errors
        return self.render_to_response(context)

    def form_valid(self, form, **kwargs):
        # take some other action here
        form.save(commit=True)
        self.request.user.profile.shop = form.instance
        self.request.user.profile.has_business = True
        self.request.user.profile.save()
        return redirect(reverse_lazy('shop-position'))
    

class ShopsListView(LoginRequiredMixin,ListView):
    template_name = 'urpsm/v2/shop/shops_list_v2.html'
    paginate_by   = 8
    model         = Shop
    context_object_name = 'shops'

    def get_queryset(self):
        try:
            city = self.request.user.profile.shop.city
        except: 
            try:
                city = self.request.user.profile.server.city
            except:
                city = None

        if city:
            return Shop.objects.select_related().filter(city=city)
        else:
            return Shop.objects.select_related()
        



class ShopDetailView(LoginRequiredMixin,DetailView):
    template_name = 'urpsm/shop/detail.html'
    model = Shop
    context_object_name = 'shop'

    def get_object(self, queryset=None):
        try:
            return get_object_or_404(Shop, slug=self.kwargs.get('slug'), city=self.request.user.profile.shop.city)
        except:
            return get_object_or_404(Shop, slug=self.kwargs.get('slug'), city=self.request.user.profile.server.city)
            

    def get_context_data(self, **kwargs):
        context = super(ShopDetailView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        components_list = Component.objects.filter(
            shop=self.get_object(), sold=False, deleted=False)
        paginator = Paginator(components_list, 15)
        page = request.GET.get('page')
        try:
            components = paginator.page(page)
        except PageNotAnInteger:
            components = paginator.page(1)
        except EmptyPage:
            components = paginator.page(paginator.num_pages)
        context['components'] = components
        return self.render_to_response(context)


class ComponentDetail(LoginRequiredMixin,TemplateView):
    template_name = 'urpsm/shop/component_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ComponentDetail, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        component = get_object_or_404(Component, shop__slug=self.kwargs.get(
            'shop_slug'), deleted=False, sold=False, slug=self.kwargs.get('component_slug'))
        context['form'] = ShopContact(
            initial={'shop': component.shop.name, 'component': component.id})
        context['component'] = component
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        component = get_object_or_404(
            Component, pk=request.POST.get('component', None))
        form = ShopContact(request.POST)
        if form.is_valid() and component:
            shop = Shop.objects.get(name=form.cleaned_data['shop'])

            message = form.cleaned_data['message']
            to = shop.shop_email
            src = request.user.email
            send_mail(component.title,
                      message, src, [to], fail_silently=False)
            form = ShopContact()
        else:
            context['form'] = ShopContact(
                initial={'shop': component.shop.name, 'component': component.id})
        context['component'] = component
        context['form'] = form
        return self.render_to_response(context)

@login_required
def shop_invoices(request):
    if request.user.profile.shop is None:
        redirect(reverse_lazy('login'))
    invoices = Invoices.objects.filter(shop=request.user.profile.shop).order_by('-created')
    return render(request, "urpsm/shop/invoices.html",{'invoices':invoices})

@login_required
def generate_invoice(request,pk):
    inv = Invoices.objects.get(pk=pk)
    if inv.shop == request.user.profile.shop or request.user.is_superuser:
        amount = inv.amount
        extra_charges = InvoiceCharges.objects.filter(invoice=inv)
        for i in extra_charges:
            amount += i.charge_amount

        return render(request, 'urpsm/shop/pdfinvoice.html',
                      {"invoice": inv, "extra_charges": extra_charges, "amount": amount})

@login_required
def action_history(request):
    if not request.user.groups.filter(name='Administrator').exists():
        return HttpResponse("Administrator only", status=403)

    history = ActionHistory.objects.filter(shop=request.user.profile.shop)
    return render(request,"urpsm/shop/actionhistory.html",{"actions":history})

@login_required
@transaction.atomic
def shop_proof_invoice(request,pk):
    if request.method == 'POST':
        if 'shop_files' in request.FILES:
            shop_files = request.FILES.getlist('shop_files')
            invoice = Invoices.objects.get(pk=pk,shop=request.user.profile.shop)
            for shop_file in shop_files:
                file_ext = shop_file.name.split(".")[-1].lower()
                new_file = SFileUpload.objects.create(actual_file_name=shop_file.name, uploaded_file=shop_file,
                                                     file_extension_name=file_ext)
                invoice.files_shop.add(new_file)
            invoice.status = 'UNPAID'
            invoice.sec_code = request.POST['seccode']
            invoice.save()
            try:
                subject = "[URPSM]Notification: Shop proof uploaded"
                content = "Proof uploaded for invoice {0} which amounts to ${1}. Please check and verify".format(invoice.id,invoice.amount)
                send_mail(subject, content, "notifications@urpsm.com", [ "billing@urpsm.com", ], fail_silently=False)
                print(content)
            except:pass
            try:
                ActionHistory.objects.create(shop=request.user.profile.shop,
                                             action="Invoice proof uploaded #" + invoice.id,
                                             user=request.user)
            except Exception:
                pass
            success_msg = "Proof Uploaded ! Now wait for admin to verify Proof "
            return render(request, 'urpsm/shop/invoice_upload.html', {'invoice': invoice,"success_msg":success_msg})
    if request.user.profile.shop:
        inv = Invoices.objects.get(pk=pk,shop=request.user.profile.shop)
        if inv.admin_comments:
            info_msg = inv.admin_comments
            return render(request,'urpsm/shop/invoice_upload.html',{'invoice':inv,'info_msg':info_msg})
        return render(request, 'urpsm/shop/invoice_upload.html', {'invoice': inv})

def gen_secret(invoiceid):
    return hashlib.sha224("sbuhbdyu@!#9821sj8!@#@"+str(invoiceid)).hexdigest()[:10]


def bitcoin_callback(request,invoice,secret):
    bw = BitcoinKeyInvoiceDict.objects.get(id=int(invoice))
    invoice = bw.invoice
    if invoice.status == 'PAID':
        return HttpResponse("*ok*",status=200)
    conf = request.GET['confirmations']
    tx = request.GET['transaction_hash']
    precomp_secret = gen_secret(bw.id)
    if precomp_secret == secret:
        if int(conf) > 3:
            value = float(request.GET['value']) / 100000000
            currency_conv = to_btc('USD',2000.00)
            invoice.amount = Decimal(value *2000/currency_conv)
            invoice.status = 'PAID'
            shop = invoice.shop
            shop.balance += Decimal(invoice.amount)
            shop.save()
            invoice.save()
            a = BitcoinHistory.objects.get(invoice=invoice)
            a.status = 'PAID'
            a.txhash = tx
            a.time_updated = timezone.now()
            a.active = False
            a.save()
            mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                   ctx={'notification': 'Bitcoin payment received, invoice #' + str(
                       invoice.id)+'. TX Hash:'+tx},
                   recipient=shop.shop_email,
                   fromemail="notifications@urpsm.com")
            mailer("urpsm/notifications/email_notifications.html", "URPSM: Payment received",
                   ctx={'notification': 'Bitcoin payment received, invoice #' + str(
                       invoice.id)+'. Please verify. TX Hash:'+tx},
                   recipient="admin@urpsm.com",
                   fromemail="notifications@urpsm.com")
            return HttpResponse("*ok*",status=200)
        return HttpResponse("Try Again",status=500)
    return HttpResponse("Invalid response",status=500)


class DepositView(LoginRequiredMixin,GroupRequiredMixin, TemplateView):
    template_name = 'urpsm/shop/deposit.html'
    group_required = u'Administrator'

    def get_context_data(self, **kwargs):
        context = super(DepositView, self).get_context_data(**kwargs)
        return context

    def post(self,request,*args,**kwargs):
        amount = request.POST['amount']
        if int(amount)>=20:
            method = request.POST['method']
            inv  = Invoices.objects.create(amount=int(amount),method=method,shop=request.user.profile.shop)
            inv.save()
            if method == 'BITCOIN':
                gap = BitcoinHistory.objects.filter(active=True,status='UNPAID')
                if gap.count() > 15:
                    oldest_tx = gap.order_by('-time_created').first()
                    if timezone.now() - oldest_tx.time_created > timezone.timedelta(hours=5):
                        oldest_tx.active = False
                        oldest_tx.save()
                        key = oldest_tx.key
                        key.invoice = inv
                        key.save()
                        oldest_tx.key = None
                        oldest_tx.save()
                        address = oldest_tx.key.address
                        BitcoinHistory.objects.create(invoice=inv,key=key,address=address)
                    else:
                        return HttpResponse("Bitcoin Transcations reached max limit try after 1 hour")
                else:
                    nw = BitcoinKeyInvoiceDict.objects.create(invoice=inv,address='-',index='-')
                    url = "https://urpsm.com"+  reverse("bitcoin-callback", kwargs=dict(invoice=nw.id,secret=gen_secret(nw.id)))
                    recv = receive(os.getenv('XPUB'), url, os.getenv('API_KEY'))
                    address = recv.address
                    nw.address = address
                    nw.index = recv.index
                    nw.save()
                    BitcoinHistory.objects.create(invoice=inv,key=nw,address=address)
                text = "Send the payment to the following unique address that has been generated for you:<br><b>"+address+"</b><br>This address will be valid for the next 4 hours. Alternatively scan the QR"
                text += "<img src='https://blockchain.info/qr?data="+address+"&size=256' >"
                print(text)
                text = mark_safe(text)
                mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                       ctx={'notification': text},
                       recipient=request.user.profile.shop.shop_email,
                       fromemail="notifications@urpsm.com")
            else:
                text = mark_safe(base64.b64decode(KeyValueStore.objects.get(category="Deposit Infos",title=inv.method).value))
            return render(request,'urpsm/shop/paymentmethods.html',{"method":inv.method,"text":text})

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "item_name": "name of the item",
            "invoice": random(),
            "notify_url": ("%s://%s%s") % (request.scheme, request.get_host(), reverse('paypal-ipn')),
            "return_url": "https://www.urpsm.com/",
            "cancel_return": "https://www.urpsm.com/",
            "custom": json.dumps({'shop_uuid': str(request.user.profile.shop.uuid), 'username': request.user.username})
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        context['form'] = form

        westernHtml = KeyValueStore.objects.get(key='westernHtml').value
        moneygramHtml = KeyValueStore.objects.get(key='moneygramHtml').value
        wafacashHtml = KeyValueStore.objects.get(key='wafacashHtml').value
        bankHtml = KeyValueStore.objects.get(key='bankHtml').value
        paypalHtml = KeyValueStore.objects.get(key='paypalHtml').value
        bitcoinHtml = KeyValueStore.objects.get(key='bitcoinHtml').value
        context['paypalHtml']=mark_safe(base64.b64decode(paypalHtml))
        context['bankHtml']=mark_safe(base64.b64decode(bankHtml))
        context['wafacashHtml']=mark_safe(base64.b64decode(wafacashHtml))
        context['moneygramHtml']=mark_safe(base64.b64decode(moneygramHtml))
        context['westernHtml']=mark_safe(base64.b64decode(westernHtml))
        context['bitcoinHtml']=mark_safe(base64.b64decode(bitcoinHtml))

        return self.render_to_response(context)
        
from app.search.backends import get_search_backend

class PublicShopSearchView(TemplateView, AjaxListView):
    template_name               = 'urpsm/v2/public/search_shops_v2.html'
    model                       = Shop
    context_object_name         ='shops'
    page_template               = "urpsm/v2/public/search_shops_result_box_v2.html"
    object_list                 = []
    
    def get(self, request, *args, **kwargs):
        query                   = request.GET.get('q', '')
        city                    = request.GET.get('city', None)
        country                 = request.GET.get('country', None)
        order_criterion         = request.GET.get('order_by', '-average_rating')
        context                 = self.get_context_data()
        if city:
            if country:
                query = "%s %s" % (city, country)
                context['city'] = city
                context['country'] = country
            else:
                query = city
                context['city'] = city
        backend                 = get_search_backend('default')
        shops                   = self.model.objects.filter(blocked=False).order_by(order_criterion)
        results                 = backend.search(query, model_or_queryset=shops, operator="or")
        context['query']        = query
        context['shops']        = results
        context['result_count'] = len(results)
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context                  = super(PublicShopSearchView, self).get_context_data(**kwargs)
        context['page_template'] = self.page_template
        context['object_list']   = self.object_list
        return context

class ShopSearchView(LoginRequiredMixin, HasBusinessMixin, PublicShopSearchView):
    template_name               = 'urpsm/v2/search/shop_search_result_v2.html'
    page_template               = "urpsm/v2/search/shop_search_result_box_v2.html"
