from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from app.notifications.models import Notification
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.utils.translation import activate
from django.views.generic import ListView, TemplateView
from braces.views import LoginRequiredMixin
from app.account.views import HasBusinessMixin
import json
from django.contrib.admin.views.decorators import staff_member_required
from app.shop.models import Shop
from app.server.models import Server

class NotificationHubView(LoginRequiredMixin,TemplateView):
    template_name = "urpsm/v2/notifications/notifications_hub_v2.html"
    # model = Notification

    def get_unread_notification_count(self, request, *args, **kwargs):
        shop = kwargs.get('shop', None)
        server = kwargs.get('server', None)
        order = kwargs.get('order', None)
        client = kwargs.get('client', None)
        ticket = kwargs.get('ticket', None)
        component = kwargs.get('component', None)
        brand = kwargs.get('brand', None)
        model = kwargs.get('model', None)
        admin = kwargs.get('admin', None)
        review = kwargs.get('review', None)
        payment = kwargs.get('payment',None)
        invoice = kwargs.get('invoice',None)
        #group = request.user.groups.values_list('name', flat=True)
        messages = kwargs.get('messages',None)
        usr = kwargs.get('user',None)

        if shop:
            if messages:
                return Notification.objects.filter(
                    to_user= usr,
                    notification_type=Notification.MESSAGE_USER,
                    is_read=False
                ).count() or 0
            if order:
                return Notification.objects.filter(
                        shop=request.user.profile.shop, 
                        notification_type__in=Notification.ORDER_WHO_TO_NOTIFY['shop'], 
                        is_read=False).exclude(server_order__isnull=True).count() or 0

            if client:
                return Notification.objects.filter(
                        shop=request.user.profile.shop,
                        notification_type__in = Notification.CLIENT_WHO_TO_NOTIFY['shop'], 
                         is_read=False).exclude(client__isnull=True).count() or 0

            if ticket:
                return Notification.objects.filter(
                        shop=request.user.profile.shop,
                        notification_type__in=Notification.TICKET_WHO_TO_NOTIFY['shop'], 
                         is_read=False).exclude(ticket__isnull=True).count() or 0

            if component:
                return Notification.objects.filter(
                        shop=request.user.profile.shop, 
                        notification_type__in=Notification.COMPONENT_WHO_TO_NOTIFY['shop'], 
                        is_read=False).exclude(component__isnull=True).count() or 0

            if brand:
                return Notification.objects.filter(
                        shop=request.user.profile.shop,
                        notification_type__in=Notification.PHONE_WHO_TO_NOTIFY['shop'], 
                         is_read=False).exclude(brand__isnull=True).count() or 0

            if model:
                return Notification.objects.filter(
                        shop=request.user.profile.shop,
                        notification_type__in=Notification.PHONE_WHO_TO_NOTIFY['shop'], 
                         is_read=False).exclude(model__isnull=True).count() or 0

            if admin:
                return Notification.objects.filter(
                        shop=request.user.profile.shop,
                        notification_type__in=Notification.ADMIN_WHO_TO_NOTIFY['shop'], 
                        is_read=False).exclude(message__isnull=True).count() or 0

            if review:
                return Notification.objects.filter(
                        shop=request.user.profile.shop,
                        notification_type__in=Notification.REVIEW_WHO_TO_NOTIFY['shop'], 
                        is_read=False).exclude(shop_review__isnull=True).count() or 0
            if invoice:
                return  Notification.objects.filter(
                        shop=request.user.profile.shop,
                        notification_type__in=Notification.INVOICE_WHO_TO_NOTIFY['shop'],
                        is_read=False).count() or 0
        #SERVER
        if server:
            if messages:
                return Notification.objects.filter(
                    to_user=usr,
                    notification_type=Notification.MESSAGE_USER,
                    is_read=False).count() or 0
            if order:
                return Notification.objects.filter(
                        server=request.user.profile.server, 
                        notification_type__in=Notification.ORDER_WHO_TO_NOTIFY['server'], 
                        is_read=False).exclude(server_order__isnull=True).count() or 0
            if ticket:
                return Notification.objects.filter(
                        server=request.user.profile.server,
                        notification_type__in=Notification.TICKET_WHO_TO_NOTIFY['server'], 
                         is_read=False).exclude(ticket__isnull=True).count() or 0

            if component:
                return Notification.objects.filter(
                        server=request.user.profile.server, 
                        notification_type__in=Notification.COMPONENT_WHO_TO_NOTIFY['server'], 
                        is_read=False).exclude(component__isnull=True).count() or 0

            if brand:
                return Notification.objects.filter(
                        server=request.user.profile.server,
                        notification_type__in=Notification.PHONE_WHO_TO_NOTIFY['server'], 
                         is_read=False).exclude(brand__isnull=True).count() or 0

            if model:
                return Notification.objects.filter(
                        server=request.user.profile.server,
                        notification_type__in=Notification.PHONE_WHO_TO_NOTIFY['server'], 
                         is_read=False).exclude(model__isnull=True).count() or 0

            if admin:
                return Notification.objects.filter(
                        server=request.user.profile.server,
                        notification_type__in=Notification.ADMIN_WHO_TO_NOTIFY['server'], 
                        is_read=False).exclude(message__isnull=True).count() or 0

            if review:
                return Notification.objects.filter(
                        server=request.user.profile.server,
                        notification_type__in=Notification.REVIEW_WHO_TO_NOTIFY['server'], 
                        is_read=False).exclude(server_review__isnull=True).count() or 0

            if payment:
                return Notification.objects.filter(
                        server=request.user.profile.server,
                        notification_type__in=Notification.PAYMENT_WHO_TO_NOTIFY['server'], 
                        is_read=False).exclude(shop_review__isnull=True).count() or 0



    def get_context_data(self, **kwargs):
        context = super(NotificationHubView, self).get_context_data(**kwargs)
        if self.request.user.profile.shop:
            context['orders'] = self.get_unread_notification_count(self.request, shop=True, order=True)
            context['clients'] = self.get_unread_notification_count(self.request, shop=True, client=True)
            context['tickets'] = self.get_unread_notification_count(self.request, shop=True, ticket=True)
            context['reviews'] = self.get_unread_notification_count(self.request, shop=True, review=True)
            # context['shops'] = 
            context['components'] = self.get_unread_notification_count(self.request, shop=True, component=True)
            context['phones'] = self.get_unread_notification_count(self.request, shop=True, brand=True) + self.get_unread_notification_count(self.request, shop=True, model=True)
            # context['servers'] = 
            context['shops'] = self.get_unread_notification_count(self.request, shop=True, admin=True)
            context['invoice'] = self.get_unread_notification_count(self.request,shop=True, invoice=True)
            context['messages'] = self.get_unread_notification_count(self, shop=True,messages=True,user=self.request.user)
            return context
        if self.request.user.profile.server:
            context['orders'] = self.get_unread_notification_count(self.request, server=True, order=True)
            context['clients'] = self.get_unread_notification_count(self.request, server=True, client=True)
            context['tickets'] = self.get_unread_notification_count(self.request, server=True, ticket=True)
            context['reviews'] = self.get_unread_notification_count(self.request, server=True, review=True)
            context['servers'] = self.get_unread_notification_count(self.request, server=True, admin=True)
            # context['servers'] =
            context['payments'] = self.get_unread_notification_count(self.request, server=True, payment=True)
            context['messages'] = self.get_unread_notification_count(self, server=True, messages=True,user=self.request.user)
            return context



class NotificationListView(LoginRequiredMixin,ListView):
    # template_name = "urpsm/v2/notifications/notifications_list_v2.html"
    model                 = Notification
    context_object_name   = 'notifications'
    paginate_by           = 10
    type                  = []
    ajax                  = False
    def __init__(self, type, ajax=False, *args, **kwargs):
        super(NotificationListView, self).__init__(*args, **kwargs )
        self.type = type
        if ajax:
            self.ajax = True
    def get_queryset(self):
        if self.request.user.profile.shop:
            return Notification.objects.filter(shop=self.request.user.profile.shop, notification_type__in=self.type)
        elif self.request.user.profile.server:
            return Notification.objects.filter(server=self.request.user.profile.server, notification_type__in=self.type)
        else:
            Notification.objects.none()

    def get(self, *args, **kwargs):
        if self.ajax:
            q = self.get_queryset().values_list()
            return HttpResponse(json.dumps(q), content_type="application/json" )
        return super(NotificationListView, self).get(*args, **kwargs)
        


@login_required
def notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user)#.values('notification_type', 'is_read','from_user', 'to_user', 'feed')
    try:
        return render(request, 'urpsm/v2/notifications/notifications_list_v2.html', {'notifications': notifications})
    except:
        return render(request, 'urpsm/v2/notifications/notifications_list_v2.html', {'notifications': []})

@login_required
def last_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user, is_read=False)[:5]
    for notification in notifications:
        notification.is_read = True
        notification.save()
    # return render(request, 'activities/last_notifications.html', {'notifications': notifications})
    return render(request, 'urpsm/notifications/last_notifications.html', {'notifications': notifications})

@login_required
def check_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user, is_read=False).count()
    return HttpResponse(notifications, content_type="application/json")

@csrf_exempt
@login_required
def markread_view(request):
    id = request.POST['notif_id']
    if request.user.profile.server:
        notif = Notification.objects.get(pk=id,server=request.user.profile.server)
    elif request.user.profile.shop:
        notif = Notification.objects.get(pk=id,shop=request.user.profile.shop)
    notif.is_read = True
    notif.save()
    return HttpResponse("Marked read!",status=200)

@csrf_exempt
@login_required
def markread_bytype_view(request):
    id = request.POST['type']
    if request.user.profile.server:
        notif = Notification.objects.filter(to_user=request.user,notification_type=id,server=request.user.profile.server)
    elif request.user.profile.shop:
        notif = Notification.objects.filter(to_user=request.user,notification_type=id,shop=request.user.profile.shop)
    for i in notif:
        i.is_read = True
        i.save()
    return HttpResponse("Marked read!",status=200)


@staff_member_required
@login_required
def send_notification(request):
    # print reque:st.POST
    try:
        shop_id = request.POST.get('shop',None)
        server_id = request.POST.get('server',None)
        notification = request.POST.get('notification',None)
        notification_type = request.POST.get('notification_type',None)
        if shop_id:
            shop = Shop.objects.get(pk=int(shop_id))
            users = User.objects.filter(profile__shop=shop)
            for user in users:
                user.profile.notify_shop_by_admin(shop)
        if server_id:
            server = Server.objects.get(pk=int(server_id))
            users = User.objects.filter(profile__server=server)
            for user in users:
                user.profile.notify_server_by_admin(server)
        return HttpResponse(json.dumps({'status':True}), content_type="application/json")
    except Exception as e:
        return HttpResponse(json.dumps({'status':False, "error":e}), content_type="application/json")
