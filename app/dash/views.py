import arrow
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, DetailView, FormView, ListView
from django.contrib.auth.models import User
from django.http import Http404
from django.http.response import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.core.urlresolvers import  reverse, reverse_lazy
from django.core.mail import send_mail
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.safestring import mark_safe
from django.db.models import Count, Max
from django.utils.translation import ugettext_lazy as _
from django.db.models.aggregates import Sum

from app.account.utils import mailer
from app.payment.models import DEBIT
from app.shop.models import Shop, Invoices, InvoiceCharges
from app.component.models import Component
from braces.views import LoginRequiredMixin
from app.client.models import Client
from datetime import datetime
from django.utils import timezone
import random
import arrow
from mobilify.settings import DEFAULT_FROM_EMAIL
from app.phone.models import Brand
from app.notifications.models import Notification
from app.shop.models import Shop
from app.server.models import Server, ServerSales
from app.ticket.models import OrderTicket, TicketMessage
from app.order.models import ServerOrder, COMPLETED, CANCELLED, REJECTED, Charges
from app.ureview.models import ShopReview, ServerReview
from app.order.models import ShopOrder
from el_pagination.views import AjaxListView
from simplecities.models import City, Country
from app.account.views import HasBusinessMixin
from .forms import ContactAdminForm
from .models import ContactAdmin, KeyValueStore, AdminActionHistory, MessageThread, Message
from app.payment import utils as payment_utils


@login_required
def AdminSupportTicket(request,pk):
    if not request.user.is_superuser:
        redirect(reverse_lazy('login'))
    ticket = get_object_or_404(OrderTicket, pk=pk)
    ticket_messages = TicketMessage.objects.filter(order_ticket=ticket)
    order = ticket.server_order
    return render(request,"urpsm/v2/dash/customOrderReply.html",{'ticket':ticket,'ticket_messages':ticket_messages,'order':order},status=200)

@login_required
def AdminViewActionHistory(request):
    if not request.user.is_superuser:
        redirect(reverse_lazy('login'))
    history = AdminActionHistory.objects.all().order_by('-created')
    return render(request,"urpsm/v2/dash/adminhistory.html",{"actions":history})

@login_required
def edit_meta(request):
    if not request.user.is_superuser:
        redirect(reverse_lazy('login'))
    if request.method == 'POST':
        url = request.POST['url']
        value = request.POST[url]
        kv = KeyValueStore.objects.get(pk=int(url))
        kv.value = value
        kv.save()
    urls = KeyValueStore.objects.filter(category='MetaTags')
    return render(request,'urpsm/v2/dash/metaedit.html',{"urls":urls})

@login_required
@csrf_exempt
def edit_site_texts(request):
    if not request.user.is_superuser:
        redirect(reverse_lazy('login'))

    if request.method == 'POST':
        for id in request.POST.keys():
            AdminActionHistory.objects.create(action="Deposit Text edited", user=request.user, affected="")

            t = KeyValueStore.objects.get(pk=id)
            t.value = request.POST[id]
            t.save()
    texts = KeyValueStore.objects.filter(category="Deposit Texts")
    ret_texts = []
    for text in texts:
        ret_texts.append({'id': text.id, 'title': text.title, 'value': mark_safe(text.value)})
    return render(request,"urpsm/v2/dash/urpsm_texts.html",{"texts":ret_texts})

@login_required
@csrf_exempt
def edit_deposit_info(request):
    if not request.user.is_superuser:
        redirect(reverse_lazy('login'))

    if request.method == 'POST':
        for id in request.POST.keys():
            AdminActionHistory.objects.create(action="Deposit Info edited", user=request.user, affected="")

            t = KeyValueStore.objects.get(pk=id)
            t.value = request.POST[id]
            t.save()
    texts = KeyValueStore.objects.filter(category="Deposit Infos")
    ret_texts = []
    for text in texts:
        ret_texts.append({'id': text.id, 'title': text.title, 'value': mark_safe(text.value)})
    return render(request, "urpsm/v2/dash/deposit_info_text.html", {"texts": ret_texts})


@csrf_exempt
@login_required
@transaction.atomic
def view_clearance_requests(request):
    if not request.user.is_superuser:
        redirect(reverse_lazy('login'))

    if request.method == 'POST':
        clearance_id = request.POST['clear']
        obj = ServerSales.objects.get(id=clearance_id,active=True)
        s_obj = ServerSales.objects.get(server=obj.server,type="available_withdraw",active=True)
        t_obj = ServerSales.objects.get(server=obj.server,type="amount_completed",active=True   )
        if t_obj.value < obj.value:
            return HttpResponse('Not enough available order balance available')
        t_obj.value -= obj.value
        s_obj.value = obj.value
        obj.active = False
        ServerSales.objects.create(server=obj.server,type="askedfor_clearance",active=True,value=Decimal(0.0))
        obj.save()
        s_obj.save()
        t_obj.save()
        AdminActionHistory.objects.create(action="Clearance request for "+str(obj.value)+" cleared #"+str(obj.id), user=request.user, affected="")
        '''
        notification = 'URPSM # has cleared amount  $' + str(obj.value) + ' for withdrawl.'
        mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
               ctx={
                   'notification': notification},
               recipient=obj.server.server_email,
               fromemail="notifications@urpsm.com")
        '''
        return HttpResponse("Cleared",status=200)

    charges = ServerSales.objects.filter(type="askedfor_clearance").exclude(value=Decimal(0.0))
    return render(request,"admin/dash/clearforwithdrawl.html",{'charges':charges})


@csrf_exempt
@login_required
@transaction.atomic()
def view_shop_invoices(request):
    if not request.user.is_superuser:
        redirect(reverse_lazy('login'))
    if request.method == 'POST':
        chargetext = request.POST['chargetext']
        chargevalue = request.POST['chargevalue']
        invoiceid = request.POST['invoice']
        invoice = Invoices.objects.get(id=invoiceid)
        if '%' in chargevalue:
            charge_amount = invoice.amount * Decimal(chargevalue[:-1])/100
        else:
            charge_amount = Decimal(chargevalue)
        if invoice.shop.balance < charge_amount:
            return HttpResponse("Shop balance is less than the charge amount. Transcation rejected. Please try again")
        AdminActionHistory.objects.create(action="Charge added to invoice, amount:"+str(chargevalue)+ ", id:"+str(invoice.id), user=request.user, affected="Invoice")
        invoice.shop.balance -= charge_amount
        invoice.shop.save()
        InvoiceCharges.objects.create(invoice=invoice,charge_text=chargetext,charge_amount=charge_amount)
        payment_utils.create_shop_payment_transaction(invoice.shop,charge_amount,invoice.shop.balance,DEBIT,chargetext + " against invoice #"+str(invoice.id))
        extra_charges = InvoiceCharges.objects.filter(invoice=invoice)
        amount = invoice.amount
        for i in extra_charges:
            amount += i.charge_amount

        return render(request, 'urpsm/shop/pdfinvoice.html', {"invoice": invoice,"extra_charges":extra_charges,"amount":amount})
    invoices = Invoices.objects.all().order_by('-created')
    return render(request, "admin/shop/shop_view_invoice.html", {'invoices': invoices})

@login_required
def urpsm_charges(request):
    if not request.user.is_superuser:
        redirect(reverse_lazy('login'))
    if request.method == 'POST':
        forall_cancel = request.POST['order_cancellation_charges_forall']
        order_cancellation_charge = request.POST['order_cancellation_charges']
        charge = Charges.objects.get(charge='order_cancellation_charges')
        charge.value = order_cancellation_charge
        charge.save()
        if forall_cancel == 'true':
            shops = Shop.objects.all()
            for shop in shops:
                if shop.cancellation_charges is not None:
                    shop.cancellation_charges = None
                    shop.save()
        AdminActionHistory.objects.create(action="URPSM Charges altered", user=request.user, affected="Charges")
        forall_complete = request.POST['order_shop_completion_charges_forall']
        order_completion_charge = request.POST['order_shop_completion_charges']
        charge = Charges.objects.get(charge='order_shop_completion_charges')
        charge.value = order_completion_charge
        charge.save()
        if forall_complete == 'true':
            shops = Shop.objects.all()
            for shop in shops:
                if shop.completion_charges is not None:
                    shop.completion_charges = None
                    shop.save()

        forall_complete = request.POST['order_completion_charges_forall']
        order_completion_charge = request.POST['order_completion_charges']
        charge = Charges.objects.get(charge='order_completion_charges')
        charge.value = order_completion_charge
        charge.save()
        if forall_complete == 'true':
            servers = Server.objects.all()
            for server in servers:
                if server.completion_charges is not None:
                    server.completion_charges = None
                    server.save()
        return render(request, 'admin/dash/charges.html')
    else:
        c_complete_charge= Charges.objects.get(charge='order_completion_charges').value
        c_cancel_charge = Charges.objects.get(charge='order_cancellation_charges').value
        c_shop_complete_charge = Charges.objects.get(charge='order_shop_completion_charges').value
        return render(request,'admin/dash/charges.html',
                      {'current_order_cancellation_charges':c_cancel_charge,
                       'current_order_completion_charges':c_complete_charge,
                       'order_shop_completion_charges':c_shop_complete_charge
                       })

@login_required
def verify_shop_proof(request,pk):
    if not request.user.is_superuser:
        redirect(reverse_lazy('login'))
    if request.method == 'POST':
        action = request.POST['action']
        inv = Invoices.objects.get(pk=pk)
        if inv.status == 'PAID':
            redirect(reverse_lazy('view-shop-invoices'))
        usr = User.objects.filter(profile__shop=inv.shop)[0]
        if action == 'MARKPAID':
            inv.status = 'PAID'
            inv.proof_upload_date = timezone.now()
            shop = inv.shop
            shop.balance += Decimal(inv.amount)
            shop.save()
            inv.save()
            AdminActionHistory.objects.create(action="Invoice id:"+str(inv.id)+", proof verified amount:"+str(inv.amount), user=request.user, affected="")
            Notification.objects.create(from_user=request.user,
                                        to_user=usr,
                                        shop=shop, invoice=inv,
                                        notification_type=Notification.INVOICE_PROOF_VERIFIED)
            success_msg = "Marked as PAID"
            return render(request, 'admin/shop/shop_verify_invoice.html', {'invoice': inv,"success_msg":success_msg})
        elif action == 'REUPLOAD':
            inv.status = 'REUPLOAD'
            inv.save()
            success_msg = "Marked for reupload"
            Notification.objects.create(from_user=request.user,
                                        to_user=usr,
                                        shop=inv.shop, invoice=inv,
                                        notification_type=Notification.INVOICE_PROOF_REUPLOAD)
            return render(request, 'admin/shop/shop_verify_invoice.html', {'invoice': inv, "success_msg": success_msg})
    else:
        inv = Invoices.objects.get(pk=pk)
        return render(request,'admin/shop/shop_verify_invoice.html',{'invoice':inv})


class AdminThankYouView(LoginRequiredMixin,TemplateView):pass

@login_required
def message_thread(request,id):
    msg_thread = MessageThread.objects.get(id=id)
    if (request.user.profile.shop and request.user.profile.shop == msg_thread.shop) or (request.user.profile.server and request.user.profile.server == msg_thread.server):
        if request.method == 'POST':
            msg = request.POST['message']
            Message.objects.create(thread=msg_thread,message=msg,from_user=request.user)
        messages = Message.objects.filter(thread=msg_thread).order_by('datetime')
        return render(request, "urpsm/v2/dash/chathistory.html", {'messages': messages,'subject':msg_thread.subject})

    if request.user.is_superuser:
        if request.method == 'POST':
            msg = request.POST.get('message','')
            email = msg_thread.shop.shop_email if msg_thread.shop else msg_thread.server.server_email
            is_solved = request.POST.get('is_solved',None)
            if is_solved == 'true':
                msg_thread.status = 'SOLVED'
                msg_thread.active = False
                msg_thread.save()
                if msg == '':
                    msg = '<i>(Issue solved and closed)</i>'
                    msg = mark_safe(msg)
            a = Message.objects.create(thread=msg_thread,message=msg,from_user=request.user)
            lastmsgtime = Message.objects.filter(thread=msg_thread,from_user=request.user).order_by('-datetime').first()
            lastmsgtime = lastmsgtime.datetime
            if a.datetime - lastmsgtime > timezone.timedelta(minutes=2,seconds=30):
                mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                       ctx={'notification': 'You have got a new admin message'},
                       recipient=email,
                       fromemail="notifications@urpsm.com")
                if msg_thread.shop:
                    us = User.objects.filter(profile__shop=msg_thread.shop)
                    for i in us:
                        Notification(shop=msg_thread.shop,message=msg,notification_type=Notification.MESSAGE_USER,to_user=i).save()
                else:
                    us = User.objects.filter(profile__server=msg_thread.server)
                    for i in us:
                        Notification(server=msg_thread.server, message=msg, notification_type=Notification.MESSAGE_USER,to_user=i).save()
        messages = Message.objects.filter(thread=msg_thread).order_by('datetime')
        return render(request, "urpsm/v2/dash/adminchathistory.html", {'cmessages': messages,'subject':msg_thread.subject})

@login_required
def new_message_from_admin(request):
    if not request.user.is_superuser:
        return ""
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        type = "ADMIN-MSG"
        to = request.POST['to']
        shop = None
        server = None
        if to == 'shop':
            shop = request.POST['shop']
        elif to == 'server':
            server = request.POST['server']
        if shop:
            shop = Shop.objects.get(id=int(shop))
            msg = MessageThread.objects.create(subject=subject, type=type, shop=shop)
            mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                   ctx={'notification': 'You have got a new admin message'},
                   recipient=shop.shop_email,
                   fromemail="notifications@urpsm.com")
            us = User.objects.filter(profile__shop=shop)
            for i in us:
                Notification(shop=shop, message=message, notification_type=Notification.MESSAGE_USER,to_user=i).save()
        elif server:
            server = Server.objects.get(id=int(server))
            msg = MessageThread.objects.create(subject=subject, type=type, server=server)
            mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                   ctx={'notification': 'You have got a new admin message'},
                   recipient=server.server_email,
                   fromemail="notifications@urpsm.com")
            us = User.objects.filter(profile__server=server)
            for i in us:
                Notification(server=server, message=message, notification_type=Notification.MESSAGE_USER,to_user=i).save()
        else:
            return ""
        Message.objects.create(thread=msg,from_user=request.user,message=message)
    messages = MessageThread.objects.all().order_by('-created_at')
    allshops = Shop.objects.all()
    allserver = Server.objects.all()
    return render(request,"urpsm/v2/dash/contact_shop_server.html",{"cmessages":messages,'allshops':allshops,'allservers':allserver})


@login_required
def newContactAdminView(request):
    template_name = 'urpsm/v2/dash/contact_admin_v2.html'
    shop = request.user.profile.shop
    server = request.user.profile.server
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        type = request.POST['type']
        if shop:
            msg = MessageThread.objects.create(subject=subject,type=type,shop=shop)
        elif server:
            msg = MessageThread.objects.create(subject=subject,type=type,server=server)
        else:
            return ""
        Message.objects.create(thread=msg,from_user=request.user,message=message)
        mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
               ctx={'notification': 'You have got a new message from '+request.user.username},
               recipient="admin@urpsm.com",
               fromemail="notifications@urpsm.com")
        return redirect(reverse('message-thread',kwargs={'id':msg.id}))
    if shop:
        messages = MessageThread.objects.filter(shop=shop)
    elif server:
        messages = MessageThread.objects.filter(server=server)
    return render(request,template_name,context={'messages':messages})

class ContactAdminView(LoginRequiredMixin,FormView, ListView):
    form_class = ContactAdminForm
    template_name = 'urpsm/v2/dash/contact_admin_v2.html'
    success_url   = reverse_lazy('adminthankyou')
    model = ContactAdmin
    paginate_by = 5
    context_object_name = "messages"
    object_list = []

    def get(self, *args, **kwargs):
        super(ContactAdminView, self).get(*args, **kwargs)
        context             = self.get_context_data(**kwargs)
        form_class          = self.get_form_class()
        form                = self.get_form(form_class)
        context['form']     = form
        # context['messages'] = ContactAdmin.objects.filter(user=self.request.user)
        return self.render_to_response(context)
        
    def form_valid(self, form):
        if form.is_valid():
            feedback =unicode(_('We had received your message. Thank you'))
            subject = "[URPSM]: %s"  % form.cleaned_data['subject']
            try:
                mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                       ctx={'notification': 'We had received your message. Thank you'},
                       recipient=form.instance.user.email,
                       fromemail="notifications@urpsm.com")
                mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                       ctx={'notification': 'Received new message from '+form.instance.user.username},
                       recipient="admin@urpsm.com",
                       fromemail="notifications@urpsm.com")
            except:pass
            form.instance.user = self.request.user
            contact = form.instance.save()
        return  redirect(self.success_url)
    def form_invalid(self, form, **kwargs):
        context         = self.get_context_data(**kwargs)
        context['form'] = ContactAdminForm(self.request.POST)
        # context['messages'] = ContactAdmin.objects.filter(user=self.request.user)
        print context['form'].errors
        return self.render_to_response(context)




class ShopPositionView(LoginRequiredMixin,DetailView, AjaxListView):
    template_name       = 'urpsm/v2/dash/shop_postion_v2.html'
    model               = Shop
    context_object_name ='shop'
    page_template       = "urpsm/v2/dash/shop_review_box_v2.html"
    object_list         = []

    def get(self, request, *args, **kwargs):
        if not self.request.user.profile.shop == self.get_object():
            return redirect(reverse('error-404'))
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['world_rank']   = self.object.rank
        context['country_rank'] = Shop.objects.filter(country=self.object.country, rank__lt=self.object.rank).count() + 1
        context['city_rank'] = Shop.objects.filter(city=self.object.city, rank__lt=self.object.rank).count() + 1
        # context = 
        return self.render_to_response(context)


    def get_context_data(self, **kwargs):
        context = super(ShopPositionView, self).get_context_data(**kwargs)
        context['reviews'] = ShopReview.objects.filter(shop=self.get_object()).values('pk', 'content', 'rating', 'user__username','language','creation_date',
                'client__brand__name','client__model__name', 'client__imei', 'client__model__picture').distinct().order_by('-creation_date')
        context['page_template'] =  "urpsm/v2/dash/shop_review_box_v2.html"
        return context

    def get_object(self, query_set=None):
        if self.request.user.profile.shop:
            return self.request.user.profile.shop

class Dashboard(TemplateView):
    template_name = 'admin/dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        context['30_day_registrations'] = self.thirty_day_registrations()
        context['active_accounts'] = self.active_accounts()
        context['shops_count'] = self.shops_count()
        context['components_count'] = self.components_count()
        context['latest_shops'] = self.latest_shops()
        context['latest_components'] = self.latest_components()
        context['ticket_admin_support'] = self.ticketadminsupport()
        context['server_low_credit'] = self.server_low_credit()
        context['shop_funds_proof'] = self.shop_funds_proof()
        context['clearance_requests'] = self.clearance_requests()
        context['new_messages'] = self.new_messages()
        return context

    def new_messages(self):
        return ContactAdmin.objects.filter(processed=False).count() or 0
    def ticketadminsupport(self):
        return OrderTicket.objects.filter(status="ADMIN_SUPPORT").count() or 0
    def clearance_requests(self):
        return ServerSales.objects.filter(type="askedfor_clearance",active=True).exclude(value=Decimal(0.0)).count()
    def server_low_credit(self):
        return 0
    def shop_funds_proof(self):
        a = Invoices.objects.filter(status="UNPAID")
        count = 0
        for i in a:
            if i.files_shop.all().count() > 0 :
                count+=1
        return count

    def latest_components(self):
        return Component.objects.select_related().order_by('-created')[:10]

    def latest_shops(self):
        return Shop.objects.select_related().order_by('-created')[:10]

    def active_accounts(self):
        return User.objects.select_related().filter(is_active=True).count()

    def shops_count(self):
        return Shop.objects.select_related().count()

    def components_count(self):
        return Component.objects.select_related().count()

    def thirty_day_registrations(self):
        final_data = []

        date = arrow.now()
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            count = User.objects.select_related().filter(
                date_joined__gte=date.floor('day').datetime,
                date_joined__lte=date.ceil('day').datetime).count()
            final_data.append(count)

        return final_data

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context=context)


BRANDS_COLORS= ['#65cea7', '#fc8675','#7bbdec','#f3ce85','#77b4e0','#63c7e0','#6ed1ac','#a89af1','#c7c38f','#8dc4e4','#bb7e75','#bb7e75','#cea5a5','#dab268','#aaa1ef','#f59ab9']


def get_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        mdl = classmodel.objects.create(value=Decimal(0.0), **kwargs)
        return mdl

@login_required()
@transaction.atomic
def server_sales_dash(request):
    server =  request.user.profile.server

    if server == None:
        return redirect(reverse_lazy('login'))

    available_withdraw_key = "available_withdraw"
    already_withdrawn_key = "already_withdrawn"
    amount_completed_key = "amount_completed"
    askedfor_clearance_key = "askedfor_clearance"

    available_withdraw = float(get_or_none(ServerSales, type=available_withdraw_key, server=server,active=True).value)
    already_withdrawn = float(get_or_none(ServerSales, type=already_withdrawn_key, server=server,active=True).value)
    amount_completed = float(get_or_none(ServerSales, type=amount_completed_key, server=server,active=True).value)

    upcoming_payments = Decimal(0.0)
    orders = ServerOrder.objects.filter(server=server, status="PENDING")
    for order in orders:
        upcoming_payments += order.amount
    upcoming_payments = float(upcoming_payments)

    charges = ServerSales.objects.filter(type__in=['available_withdraw', 'askedfor_clearance'], server=server).exclude(value=Decimal(0.0))

    if request.method == 'POST':
        if request.POST['action'] == 'askclearance':

            amount = float(request.POST['amount'])
            amount_completed = float(get_or_none(ServerSales,type=amount_completed_key,server=server,active=True).value)
            if (amount > amount_completed):
                return render(request, 'urpsm/v2/dash/server_sales_dashboard.html',
                              {'upcoming_payments': upcoming_payments,
                               'upcoming_payments_num': orders.count(),
                               'available_withdraw': available_withdraw,
                               'already_withdrawn': already_withdrawn,
                               'amount_completed': amount_completed,
                               'msg': 'Not enough order balance',
                               'charges': charges
                               })
            ServerSales.objects.create(type=askedfor_clearance_key,server=server,active=True,value=Decimal(amount))
            amount_completed_obj = get_or_none(ServerSales, type=amount_completed_key, server=server, active=True)
            amount_completed_obj.value -= Decimal(amount)
            amount_completed_obj.save()
            notification = 'Server #' + str(server.id) + ' has requested to clear $'+ str(amount)+' for withdrawl.'
            mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                                 ctx={
                                     'notification': notification},
                                 recipient="admin@urpsm.com",
                                 fromemail="notifications@urpsm.com")
            return render(request, 'urpsm/v2/dash/server_sales_dashboard.html',
                          {'upcoming_payments': upcoming_payments,
                           'upcoming_payments_num': orders.count(),
                           'available_withdraw': available_withdraw,
                           'already_withdrawn': already_withdrawn,
                           'amount_completed': amount_completed,
                           'msg':'Clearance requested',
                           'charges':charges
                           })
        elif request.POST['action'] == 'withdraw':
            email = request.POST['paypal-email']
            amount = ServerSales.objects.get(active=True,server=server,type="available_withdraw")
            val = amount.value
            if val == 0 or amount.active == None:
                redirect(reverse_lazy('sales-dashboard'))

            amount.desc = email
            amount.value = Decimal(0.0)

            amount.active = None
            amount.save()

            response = payment_utils.transfer_money_to_paypal_account(email,val)
            msg = response["message"]
            if response['success']:
                server.credit -= val
                server.save()
                amount.active = False
                available_withdraw = float(
                    get_or_none(ServerSales, type=available_withdraw_key, server=server, active=True).value)
                payment_utils.create_server_payment_transaction(server,val,server.credit,DEBIT,'Withdrawl to paypal id:'+email+' against '+str(amount.id))
                notification = 'Server #' + str(server.id) + ' has withdrew  $' + str(val) + ' to paypal id: ' + email
                print notification
                already_withdrawn_obj = get_or_none(ServerSales, type=already_withdrawn_key, server=server, active=True)
                already_withdrawn_obj.value += Decimal(val)
                already_withdrawn_obj.save()
            else:
                amount.active = True
            amount.value = val
            amount.save()

            charges = ServerSales.objects.filter(type__in=['available_withdraw', 'askedfor_clearance'],
                                                 server=server).exclude(value=Decimal(0.0))
            return render(request, 'urpsm/v2/dash/server_sales_dashboard.html',
                              {'upcoming_payments': upcoming_payments,
                               'upcoming_payments_num': orders.count(),
                               'available_withdraw': available_withdraw,
                               'already_withdrawn': already_withdrawn,
                               'amount_completed': amount_completed,
                               'msg': msg,
                               'charges':charges
                               })
    return render(request,'urpsm/v2/dash/server_sales_dashboard.html',
                  {'upcoming_payments':upcoming_payments,
                   'upcoming_payments_num':orders.count(),
                   'available_withdraw':available_withdraw,
                   'already_withdrawn':already_withdrawn,
                   'amount_completed':amount_completed,
                   'charges':charges
                   })
class Dash(LoginRequiredMixin,ListView):
    template_name = 'urpsm/v2/dash/shop_dashboard_v2.html'
    model         = Client
    context_object_name = 'clients'
    object_list = []
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super(Dash, self).get_context_data(*args, **kwargs)
        # the last 10 clients
        
        clients  = Client.objects.select_related().filter(deleted=False, shop=self.request.user.profile.shop)
        context['clients'] = clients[:30]

        # Clients count
        context['clients_count'] = clients.count() or 0

        # Clients count
        context['new_clients_count'] = clients.filter(created__gte=self.request.user.last_login).count() 

        # total revenues
        total = 0
        _clients = clients.filter(paid=True).exclude(status='n')
        for client in _clients:
            total += client.total_benefit
        context['revenues'] = total

        # current month revenues
        total = 0
        _clients = clients.filter(created__month=datetime.now().month).exclude(status='n')
        for client in _clients:
            total += client.total_benefit
        context['current_month_revenues'] = total

        # upcoming revenues
        total = 0
        _clients = clients.filter(paid=False).exclude(status='n')
        for client in _clients:
            total += client.total_benefit
        context['upcoming_revenues'] = total

        # not paid 
        context['not_paid'] = _clients.exclude(status='n').count() or 0


        # Components count
        components = Component.objects.select_related().filter(deleted=False)
        context['components_count'] = components.count() or 0

        # Components count
        context['new_components_count'] = components.filter(created__gte=self.request.user.last_login).count() or 0


        # mobile brand trends
        context['chart_data'] = self.brands_trends(clients)

        # Curve data
        context['thirty_day_total_revenues'] = self.thirty_day_total_revenues()
        context['thirty_day_clients'] = self.thirty_day_clients()
        context['thirty_day_components'] = self.thirty_day_components()
        context['thirty_day_upcoming_revenues'] = self.thirty_day_upcoming_revenues()
        context['thirty_day_current_month_revenues'] = self.thirty_day_current_month_revenues()
        context['thirty_day_completed_orders'] = self.thirty_day_completed_orders()
        context['thirty_day_cancelled_orders'] = self.thirty_day_cancelled_orders()
        context['thirty_day_raised_tickets'] = self.thirty_day_raised_tickets()
        return context
        return self.render_to_response(context)

    def thirty_day_total_revenues(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            clients = Client.objects.select_related().filter(
                deleted=False,
                paid=True,
                shop=self.request.user.profile.shop,
                created__gte=date.floor('day').datetime,
                created__lte=date.ceil('day').datetime).exclude(status='n')
            total = 0
            for client in clients:
                total += client.total

            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': float(total)})
        return mark_safe(final_data)

    def mobile_brand_trends(self):
        final_data = []
        brands = Client.objects.select_related().filter(
            deleted=False, shop=self.request.user.profile.shop).values('brand', 'brand__name').annotate(count=Count('brand')).order_by('-count')
        for brand in brands:
            final_data.append({
                'label': brand.get('brand__name'),
                'value': brand.get('count'),
                'color': random.choice(BRANDS_COLORS)
            })
        return final_data

    def brands_trends(self, clients):
        dump = {}
        chart_data = []
        brand = None
        for client in clients:
            if not brand:
                brand = client.brand
            elif not brand == client.brand:
                brand = client.brand
            if not brand.name in dump:
                dump[brand.name] = {}
                count = clients.filter(brand=brand).count()
                amount = float(clients.filter(brand=brand).aggregate(Sum('amount'))['amount__sum']) 
                color  = random.choice(BRANDS_COLORS)
                tooltip_text = "%s$" % (amount)
                bar_data = []
                bar_data.append(str(brand.name))
                bar_data.append(count)
                bar_data.append(color)
                bar_data.append(tooltip_text)
                chart_data.append(mark_safe(bar_data))

        return chart_data

    def thirty_day_clients(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            count = Client.objects.select_related().filter(
                deleted=False,
                # paid=True,
                shop=self.request.user.profile.shop,
                created__gte=date.floor('day').datetime,
                created__lte=date.ceil('day').datetime).exclude(status='n').count()
            
            

            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': count})
        return mark_safe(final_data)

    def thirty_day_components(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            count = Component.objects.select_related().filter(
                created__gte=date.floor('day').datetime,
                created__lte=date.ceil('day').datetime,
                deleted=False).count()
            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': count})
        return mark_safe(final_data)

    def thirty_day_upcoming_revenues(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            total = 0
            clients = Client.objects.select_related().filter(
                shop=self.request.user.profile.shop, deleted=False, paid=False,
                created__gte=date.floor('day').datetime,
                created__lte=date.ceil('day').datetime).exclude(status='n')
            for client in clients:
                total += client.total_benefit
            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': float(total)})

        return mark_safe(final_data)

    def thirty_day_current_month_revenues(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            total = 0
            clients = Client.objects.select_related().filter(
                shop=self.request.user.profile.shop, deleted=False, paid=True,
                created__month=datetime.now().month,
                created__gte=date.floor('day').datetime,
                created__lte=date.ceil('day').datetime).exclude(status='n')
            for client in clients:
                total += client.total_benefit
            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': float(total)})
            
        return mark_safe(final_data)

    def thirty_day_completed_orders(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            total = 0
            count = ServerOrder.objects.filter(shop=self.request.user.profile.shop,
             deleted=False, paid=True, 
             created__year=datetime.now().year,
             created__month=datetime.now().month,
             created__day=datetime.now().day, status=COMPLETED).count()
    
            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': count})
            
        return mark_safe(final_data)

    def thirty_day_cancelled_orders(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            count = ServerOrder.objects.filter(shop=self.request.user.profile.shop,
             deleted=False, 
             created__year=datetime.now().year,
             created__month=datetime.now().month,
             created__day=datetime.now().day, status=CANCELLED).count()
            
    
            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': count})
        return mark_safe(final_data)

    def thirty_day_raised_tickets(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            # total = 0
            count = OrderTicket.objects.select_related().filter(
                server_order__shop=self.request.user.profile.shop,
                created_at__month=datetime.now().month,
                created_at__gte=date.floor('day').datetime,
                created_at__lte=date.ceil('day').datetime).count()
    
            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': count})
            
        return mark_safe(final_data)


class ServerDash(LoginRequiredMixin,ListView):
    template_name="urpsm/v2/dash/server_dashboard_v2.html"
    networks     = []
    model        = ServerOrder
    paginate_by  = 10
    context_object_name = "orders"
    object_list  = []

    # def get_queryset(self, *args, **kwargs):
    #     return 

    def get_context_data(self, *args, **kwargs):
        context = super(ServerDash, self).get_context_data(*args, **kwargs)

        context['orders'] = ServerOrder.objects.filter(
            deleted=False, server=self.request.user.profile.server).order_by('-created')[:30]

        context['shop_orders_count'] = ServerOrder.objects.filter(
            deleted=False, server=self.request.user.profile.server).count() 

        context['new_shop_orders_count'] = ServerOrder.objects.filter(deleted=False,
         server=self.request.user.profile.server, created__gte=self.request.user.last_login).count() 

        paid_orders = ServerOrder.objects.filter(server=self.request.user.profile.server, paid=True)
        context['completed_orders_count'] = paid_orders.count() or 0
        today = datetime.now().date()
        context['today_completed_orders_count'] = ServerOrder.objects.select_related().filter(
            server=self.request.user.profile.server, status=COMPLETED, paid=True,
            delivery_time__day=today.day, delivery_time__month=today.month, delivery_time__year=today.year).count() or 0

        context['cancelled_orders_count'] = ServerOrder.objects.select_related().filter(
            server=self.request.user.profile.server, status=CANCELLED, paid=True).count() or 0

        context['today_cancelled_orders_count'] = ServerOrder.objects.select_related().filter(
            server=self.request.user.profile.server, status=CANCELLED, paid=True, 
            delivery_time__day=today.day, delivery_time__month=today.month, delivery_time__year=today.year).count() or 0

        context['raised_tickets_count'] = OrderTicket.objects.filter(server_order__server=self.request.user.profile.server).count() or 0

        context['today_raised_tickets_count'] = OrderTicket.objects.filter(
            server_order__server=self.request.user.profile.server, 
            created_at__day=today.day, created_at__month=today.month, created_at__year=today.year).count() or 0

        # total revenues
        total = 0
        orders = ServerOrder.objects.filter(
            server=self.request.user.profile.server, deleted=False, paid=True).exclude(status=REJECTED)
        for order in orders:
            total += float(order.amount)
        context['revenues'] = total

        # current month revenues
        total = 0
        orders = ServerOrder.objects.filter(
            server=self.request.user.profile.server, deleted=False, paid=True, created__month=datetime.now().month).exclude(status=REJECTED)
        for order in orders:
            total += float(order.amount)
        context['current_month_revenues'] = total

        # upcoming revenues
        total = 0
        orders = ServerOrder.objects.filter(
            server=self.request.user.profile.server, deleted=False, paid=False).exclude(status__in=[REJECTED, COMPLETED, CANCELLED])
        for order in orders:
            total += float(order.amount)
        context['upcoming_revenues'] = total

        # not paid 
        context['not_paid'] = ServerOrder.objects.filter(
            server=self.request.user.profile.server, deleted=False, paid=False).exclude(status=REJECTED).count() or 0

        context['chart_data'] = self.networks_trends(paid_orders)
        context['networks']   = self.networks


        # mobile brand trends
        # context['brands'] = self.mobile_brand_trends()

        # Curve data
        # context['thirty_day_shop_orders'] = self.thirty_day_shop_orders()
        # context['thirty_day_total_revenues'] = self.thirty_day_total_revenues()
        # context['thirty_day_upcoming_revenues'] = self.thirty_day_upcoming_revenues()
        # context['thirty_day_current_month_revenues'] = self.thirty_day_current_month_revenues()
        # context['thirty_day_completed_orders'] = self.thirty_day_completed_orders()
        # context['thirty_day_cancelled_orders'] = self.thirty_day_cancelled_orders()
        # context['thirty_day_raised_tickets'] = self.thirty_day_raised_tickets()

        return context
        return self.render_to_response(context)

    def networks_trends(self, orders):
        dump = {}
        chart_data = []
        brand = None
        for order in orders:
            brand  = order.brand
            try:
                if not brand.name in dump:
                    dump[brand.name] = {}
                    count = orders.filter(brand=brand).count()
                    amount = float(orders.filter(brand=brand).aggregate(Sum('amount'))['amount__sum'])
                    color  = random.choice(BRANDS_COLORS)
                    tooltip_text = "%s$" % (amount)
                    bar_data = []
                    bar_data.append(str(brand.name))
                    bar_data.append(count)
                    bar_data.append(color)
                    bar_data.append(tooltip_text)
                    chart_data.append(mark_safe(bar_data))
            except:
                print "brand not found for order"

        return chart_data



    
    def thirty_day_shop_orders(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            total = 0
            count = ServerOrder.objects.filter(server=self.request.user.profile.server,
             deleted=False, paid=False, 
             created__year=datetime.now().year,
             created__month=datetime.now().month,
             created__day=datetime.now().day).exclude(status__in=[REJECTED,CANCELLED])
    
            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': count})

        return mark_safe(final_data)
     

    def thirty_day_total_revenues(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            orders = ServerOrder.objects.filter(server=self.request.user.profile.server,
             deleted=False, paid=True, status=COMPLETED,
             created__year=datetime.now().year,
             created__month=datetime.now().month,
             created__day=datetime.now().day)
            total = 0
            for order in orders:
                total += order.amount

            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': float(total)})
        return mark_safe(final_data)

    def thirty_day_upcoming_revenues(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            total = 0
            orders = ServerOrder.objects.filter(server=self.request.user.profile.server,
             deleted=False, paid=False, 
             created__year=datetime.now().year,
             created__month=datetime.now().month,
             created__day=datetime.now().day).exclude(status__in=[REJECTED,CANCELLED])
            for order in orders:
                total += order.amount
    
            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': total})
            
        return mark_safe(final_data)

    def thirty_day_completed_orders(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            count = ServerOrder.objects.filter(server=self.request.user.profile.server,
             deleted=False, paid=True, 
             created__year=datetime.now().year,
             created__month=datetime.now().month,
             created__day=datetime.now().day, status=COMPLETED).count()
            
    
            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': count})
        return mark_safe(final_data)

    def thirty_day_cancelled_orders(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            count = ServerOrder.objects.filter(server=self.request.user.profile.server,
             deleted=False, paid=True, 
             created__year=datetime.now().year,
             created__month=datetime.now().month,
             created__day=datetime.now().day, status=CANCELLED).count()
            
    
            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': count})
        return mark_safe(final_data)


    def thirty_day_current_month_revenues(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            total = 0
            orders = ServerOrder.objects.filter(server=self.request.user.profile.server,
             deleted=False, paid=True, 
             created__year=datetime.now().year,
             created__month=datetime.now().month,
             created__day=datetime.now().day).exclude(status=REJECTED)
            for order in orders:
                total += order.amount
    
            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': total})
            
        return mark_safe(final_data)


    def thirty_day_raised_tickets(self):
        final_data = []
        date = arrow.now().replace(days=+1)
        for day in xrange(1, 30):
            date = date.replace(days=-1)
            # total = 0
            count = OrderTicket.objects.select_related().filter(
                server_order__server=self.request.user.profile.server,
                created_at__month=datetime.now().month,
                created_at__gte=date.floor('day').datetime,
                created_at__lte=date.ceil('day').datetime).count()
    
            final_data.append(
                {'day': date.format('YYYY-MM-DD'), 'amount': count})
            
        return mark_safe(final_data)
        
"""
OrderTicket.objects.filter(
            server_order__server=self.request.user.profile.server, 
            created_at__day=today.day, created_at__month=today.month, created_at__year=today.year)
"""


@staff_member_required
def send_feedback(request):
    try:
        contact  = request.POST['contact']
        type  = request.POST['type']
        subject  = request.POST['subject']
        feedback = request.POST['feedback']
        message = request.POST['message']
        user     = request.POST['user']
        user     = User.objects.get(pk=int(user))
        print user
        try:
            mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                   ctx={'notification': 'New Admin message #-' + message},
                   recipient=user.email,
                   fromemail="notifications@urpsm.com")
        except Exception as e:
            print e
        if user.profile.shop:
            Notification.objects.create(shop=user.profile.shop,from_user=request.user,message=feedback,to_user=user,notification_type='J')
        elif user.profile.server:
            Notification.objects.create(server=user.profile.server, from_user=request.user, message=feedback, to_user=user,
                                        notification_type='J')

        contact = ContactAdmin.objects.get(pk=int(contact))
        contact.feedback = feedback
        contact.processed = True
        contact.save()
        return JsonResponse({'status':True})
    except Exception as e:
        print e
        return JsonResponse({'status':False})