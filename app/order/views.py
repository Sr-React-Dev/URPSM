from __future__ import absolute_import
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, ListView, TemplateView
from django.core.urlresolvers import reverse_lazy
# from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render_to_response, render
from django.core.urlresolvers import reverse

from app.account.utils import mailer
from app.order.utils import get_naksh_delivery_date, update_server_order
from app.shop.models import ActionHistory
from .models import *
from .forms import ServerOrderForm
from django.http import Http404, JsonResponse, HttpResponseNotFound
from django.db.models import Q
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from app.dhrufusion.client import Client
from app.endpoint.models import Endpoint
import decimal
from app.order import utils as order_utils
from app.payment import utils as payment_utils
from app.notifications.models import Notification
from django.db import transaction
from app.payment.models import DEBIT, CREDIT
import traceback
from app.account.views import HasBusinessMixin


class ServerOrderTicketsListView(LoginRequiredMixin,ListView):
    template_name = "urpsm/v2/ticket/ticket_list_v2.html"
    model         = ServerOrder
    context_object_name   = 'tickets'
    paginate_by   = 10

    def get_queryset(self, *args, **kwargs):
        q = None
        if self.request.user.profile.shop:
            orders = ServerOrder.objects.filter(shop=self.request.user.profile.shop)
        elif self.request.user.profile.server:
            orders = ServerOrder.objects.filter(server=self.request.user.profile.server)
        else:
            return ServerOrder.objects.none()

        for order in orders:
            if not q:
                q= order.order_tickets.all()
            else:
                q = q | order.order_tickets.all()
        if q:
            return q.order_by('-created_at')
        else:
            return ServerOrder.objects.none()

@transaction.atomic
@login_required
def UnlockingViewF(request):
    template_name = 'urpsm/endpoint/unlocking.html'
    form_start = ServerOrderForm()
    group_required = [u'Administrator', u'Technician']
    '''
    try:
        endpointid = Endpoint.objects.get(server=order.sh).id
    except:
        endpointid = 1#Endpoint.objects.filter(server=request.user.profile.server)[0].id
    '''
    returnObj = []
    try:
        endpoints = Endpoint.objects.all()
        for endpoint in endpoints:
            e_name = str(endpoint.server.id)+endpoint.server.name
            networks = [(endpoint.id,x.id,x.name) for x in endpoint.networks.all()]
            if networks != []:
                returnObj.append([e_name,networks])
    except:
        returnObj = []
    if request.method == 'POST':
        if not request.user.groups.filter(name__in=['Administrator','Technician']).exists():
            return HttpResponse("Only an administrator or technician can place order",status=403)
        form = ServerOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            shop = request.user.profile.shop
            order.shop = shop
            endpoint = Endpoint.objects.get(pk=request.POST['endpoint'])
            server = endpoint.server
            order.server = server
            service = request.POST['service']
            serviceObj = endpoint.client.get_imei_service_detail_new(id=service)
            imei = request.POST['imei']

            if True:
                credit = decimal.Decimal(endpoint.get_credit())
                amount = decimal.Decimal(serviceObj['credit'])
                balance = request.user.profile.shop.balance
                if shop.completion_charges == None:
                    urpsm_charge = Charges.objects.get(charge='order_shop_completion_charges').value
                else:
                    urpsm_charge = shop.completion_charges
                if '%' in urpsm_charge:
                    urpsm_charge_amount = amount * decimal.Decimal(urpsm_charge[:-1]) / 100
                else:
                    urpsm_charge_amount = decimal.Decimal(urpsm_charge)
                amount += urpsm_charge_amount

                if amount > credit:
                    error_msg = "Amount greater than credit"
                    return render(request, template_name,
                                  {'form': form_start, 'returnObj':returnObj, 'error_msg': error_msg})

                    #return redirect(reverse('servicebusy'))

                if balance >= amount:
                    print
                    "balance is greater than amount. So Order can be placed"
                    data = json.loads(endpoint.place_order(service, imei))
                    print
                    "data for place_order in dhru: ", data
                    if   'referenceid' in data:
                        shop.balance -= decimal.Decimal(amount)
                        order.amount = decimal.Decimal(amount)
                        order.status = PENDING
                        order.service = serviceObj['title']
                        shop.save()
                        order.ref = data['referenceid']
                        order.save()
                        payment_utils.create_shop_payment_transaction(shop, amount, shop.balance, DEBIT,
                                                                      "Amount debited for order id: " + str(order.id))
                        ActionHistory.objects.create(shop=shop,action="Order placed, order id:"+str(order.id),user=request.user)
                        c = endpoint.client
                        if c.status():
                            # print service
                            order.save()
                            if endpoint.provider == 'naksh' or endpoint.provider == 'gsm':
                                order.delivery_time = get_naksh_delivery_date(serviceObj['time'])
                            order.save()
                            # Notification.objects.create(from_user=shop.user,
                            #                             to_user=server.user, server=server,
                            #                             shop=shop, server_order=order,
                            #                             notification_type=Notification.NEW_ORDER)
                            mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                                   ctx={'notification':'You\'ve got a new order '+str(order.id)}, recipient=server.server_email,
                                   fromemail="notifications@urpsm.com")
                            users = User.objects.filter(profile__server=server)
                            for user in users:
                                user.profile.notify_server_for_new_order(server, shop, order)
                                print "Notified",user.id
                                mailer("urpsm/notifications/email_notifications.html", "URPSM: Notification",
                                       ctx={'notification':'You\'ve got a new order '+str(order.id)}, recipient=user.email,
                                       fromemail="notifications@urpsm.com")
                            success_msg = "Order placed successfully."
                            return render(request, template_name,
                                          {'form': form_start, 'returnObj':returnObj,
                                           'success_msg': success_msg})
                    elif 'credit' in data:
                        error_msg = "Server credit low"
                        return render(request, template_name,
                                      {'form': form_start, 'returnObj': returnObj,
                                       'error_msg': error_msg})
                    else:
                        error_msg = "Unexpected response from the endpoint"
                        return render(request, template_name,
                                      {'form': form_start,'returnObj':returnObj,
                                       'error_msg':error_msg})
                        #return redirect(reverse('servicebusy'))
                else:
                    error_msg = "Shop balance is low"
                    return render(request, template_name,
                                  {'form': form_start, 'returnObj': returnObj,
                                   'error_msg':error_msg})
                    #return redirect(reverse('deposit'))
            else:
                return HttpResponse("Error")
        else:
            return render(request, template_name, {'form': form_start, 'returnObj': returnObj,'error_msg':'Invalid form data'})

    return render(request,template_name, {'form': form_start,'returnObj':returnObj})



class UnlockingView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    template_name = 'urpsm/endpoint/unlocking.html'
    model = ServerOrder
    form_class = ServerOrderForm
    group_required = [u'Administrator', u'Technician']

    @transaction.atomic
    def form_valid(self, form):
        order = form.save(commit=False)
        shop = self.request.user.profile.shop
        order.shop = shop
        endpoint = Endpoint.objects.get(pk=self.request.POST['endpoint'])
        server = endpoint.server
        order.server = server
        service = self.request.POST['service']
        imei = self.request.POST['imei']

        if endpoint.account_info() is not False:
            credit = decimal.Decimal(json.loads(
                endpoint.account_info())['credit'])
            amount = decimal.Decimal(json.loads(
                endpoint.service_info(id=service))['credit'])
            balance = self.request.user.profile.shop.balance
            if amount > credit:
                print "amount is greater than credit. Order can't be placed"
                return redirect(reverse('servicebusy'))

            if balance >= amount:
                print "balance is greater than amount. So Order can be placed"
                data = json.loads(endpoint.place_order(service, imei))
                print "data for place_order in dhru: ", data
                if 'referenceid' in data:
                    shop.balance -= decimal.Decimal(amount)
                    order.amount = decimal.Decimal(amount)
                    order.status = PENDING
                    shop.save()
                    order.ref = data['referenceid']
                    order.save()
                    payment_utils.create_shop_payment_transaction(shop, amount, shop.balance, DEBIT,
                                                                  "Amount debited for order id: " + order.id)
                    c = Client(dhrufusion_url=order.endpoint.url,
                               username=order.endpoint.username,
                               apiaccesskey=order.endpoint.key)
                    if c.status():
                        service = json.loads(c.get_imei_service_details(id=order.ref))
                        # print service
                        order.save()
                    # Notification.objects.create(from_user=shop.user,
                    #                             to_user=server.user, server=server,
                    #                             shop=shop, server_order=order,
                    #                             notification_type=Notification.NEW_ORDER)
                        users = User.objects.filter(profile__server=server)
                        for user in users:
                            user.profile.notify_server_for_new_order(server, shop, order)
                else:
                    return redirect(reverse('servicebusy'))
            else:
                return redirect(reverse('deposit'))
        
        return super(UnlockingView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('orders')


class ServerOrdersView(LoginRequiredMixin, ListView):
    template_name = 'urpsm/orders/index.html'
    model = ServerOrder
    context_object_name = 'orders'
    paginated_by = 15

    def get_queryset(self):
        return ServerOrder.objects.select_related().filter(shop=self.request.user.profile.shop).order_by('-created')

    def get_context_data(self, **kwargs):
        context = super(ServerOrdersView, self).get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        term = ''
        if 'q' in request.GET and request.GET.get('q').strip():
            term = request.GET.get('q').strip()
            self.object_list = self.get_queryset().filter(Q(imei__icontains=term))

        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404("Empty list and '%(class_name)s.allow_empty' is False."
                              % {'class_name': self.__class__.__name__})
        context = self.get_context_data()
        return self.render_to_response(context)


class ServerOrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'urpsm/orders/detail.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        order = get_object_or_404(ServerOrder, pk=self.kwargs.get(
            'pk'), shop=request.user.profile.shop)
        order = update_server_order(order)
        context['ref'] = order.ref
        context['order'] = order
        context['cancellation_allowed'] = order_utils.validate_server_order_for_cancellation(order)
        context['error'] = False
        c = order.endpoint.client
        if c.status():
            od = json.loads(c.get_imei_order(id=order.ref))
            if order.status == CANCELLED:
                context['orderstatus'] = 'Cancelled'
                context['statuscolor'] = '#ff9900'
            else:
                context['orderstatus'] = od.get('status')
                statuscolor = "green"
                if context['orderstatus'].lower() == PENDING.lower():
                    statuscolor = " #00ace6"
                elif context['orderstatus'] == COMPLETED.lower():
                    statuscolor = " #00e6ac"
                context['statuscolor'] = statuscolor
                context['code'] = od.get('code')
        else:
            context['error'] = True
        return self.render_to_response(context)


class ServiceDown(LoginRequiredMixin, TemplateView):
    template_name = 'urpsm/orders/service_down.html'


# create a view to get the order details


class CancelServerOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'urpsm/orders/cancel_order_page_new.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        server_order = get_object_or_404(ServerOrder, pk=self.kwargs.get(
            'pk'), shop=request.user.profile.shop)
        if not order_utils.validate_server_order_for_cancellation(server_order):
            context["error_message"] = ("Order %s is not valid for cancellation") % str(server_order.ref)
            return redirect(reverse('orders'))
        server_order = update_server_order(server_order)
        context['order'] = server_order
        statuscolor = "black"
        if server_order.status == PENDING:
            statuscolor = " #00ace6"
        elif server_order.status == CANCELLED:
            statuscolor = " #ff9900"
        elif server_order.status == COMPLETED:
            statuscolor = " #00e6ac"
        context['statuscolor'] = statuscolor
        context.update(csrf(request))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        server_order = get_object_or_404(ServerOrder, pk=self.kwargs.get(
            'pk'), shop=request.user.profile.shop)
        comments = request.POST.get('shop_comments')
        context['order']=server_order

        try:
            if request.user.profile.shop != server_order.shop:
                context['error_message'] = "Not authorized to cancel this order"
                return self.render_to_response(context)
            shop_files = None
            print "request.Files: ", request.FILES
            if 'shop_files' in request.FILES:
                shop_files = request.FILES.getlist('shop_files')
                for shop_file in shop_files:
                    print shop_file
                    print shop_file.name

            print "shop_files: ", shop_files
            order_cancellation_status = order_utils.validate_and_cancel_server_order(server_order, comments, shop_files)
            print "order_cancellation_status: ", order_cancellation_status
            if order_cancellation_status[0]:
                if order_cancellation_status[1] is None:
                    return redirect(reverse('orders'))
                else:
                    ticket = order_cancellation_status[1]
                    return redirect(reverse('ticket_detail', args=[ticket.id]))
            elif not order_cancellation_status[0]:
                context['error_message'] = "Order can't be cancelled."
                return self.render_to_response(context)
        except Exception, e:
            print(traceback.format_exc())
            context['error_message'] = "Some error Occurred"
            return self.render_to_response(context)
        context['error_message'] = "Some error Occurred"
        return self.render_to_response(context)





# @login_required
# @csrf_exempt
# def cancel_server_order(request, order_id):
#     if request.method == 'POST' and order_id is not None:
#         # order_id = request.GET.get('id')
#         # reason = request.POST.get('reason')
#         comments = request.POST.get('shop_comments')
#         order = ServerOrder.objects.get(id=order_id)
#         response = {}
#         try:
#             shop_profiles = order.shop.user_shop.all()
#             is_valid_user_for_cancellation = False
#             for profile in shop_profiles:
#                 if profile.user == request.user:
#                     is_valid_user_for_cancellation = True
#                     break
#             if not is_valid_user_for_cancellation:
#                 response['error_message'] = "Not authorized to cancel this order"
#                 return JsonResponse(response)
#             shop_files=None
#             order_cancellation_status = order_utils.validate_and_cancel_server_order(order, comments, shop_files)
#             print "order_cancellation_status: ", order_cancellation_status
#             if order_cancellation_status is None:
#                 response['error_message'] = "Error in getting Order status from DHRU"
#                 response['error'] = True
#             elif not order_cancellation_status:
#                 response['error_message'] = "Order can't be cancelled."
#                 response['error'] = True
#             else:
#                 response['success'] = True
#         except Exception, e:
#             print(traceback.format_exc())
#             response['error_message'] = "Some error Occurred"
#             response['error'] = True
#         return JsonResponse(response)
#     return HttpResponseNotFound()


