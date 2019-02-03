# Created by Vishwash Gupta
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponse
from django.http import JsonResponse
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from app.dash.models import AdminActionHistory
from app.order.utils import cancel,complete
from app.ticket import utils
from app.ticket.models import OrderTicket
from braces.views import LoginRequiredMixin
from django.views.generic import CreateView, ListView, TemplateView
from django.shortcuts import redirect, get_object_or_404
from .models import *
from django.core.urlresolvers import reverse, reverse_lazy
import utils as ticket_utils
from django.db import transaction
from app.account.views import HasBusinessMixin


class TicketDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'urpsm/tickets/ticket_details.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        ticket = get_object_or_404(OrderTicket, pk=self.kwargs.get(
            'pk'))
        if 'success_message' in self.kwargs:
            context['success_message'] = self.kwargs.get('success_message')
        ticket_messages = TicketMessage.objects.filter(order_ticket=ticket)
        # print ticket_messages, len(ticket_messages)
        context['ticket'] = ticket

        context['ticket_messages'] = ticket_messages
        context.update(csrf(request))
        return self.render_to_response(context)

    @csrf_exempt
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        order_ticket = get_object_or_404(OrderTicket, pk=self.kwargs.get(
            'pk'))
        context['ticket'] = order_ticket
        action = response = request.POST['action']
        # if ticket response is given by server owner
        if action == 'ticket_response':
            server_order = order_ticket.server_order
            print request.POST
            response = request.POST.get('response', None)
            reason = request.POST.get('reason', None)
            admin_support_reason = request.POST.get('admin_support_reason', None)
            print response, reason, admin_support_reason
            if response is None or response not in [COMPLETED, ADMIN_SUPPORT, CANCELLED]:
                context['error_message'] = "Invalid response"
                return self.render_to_response(context)

            if request.user.profile.shop == server_order.shop:
                if order_ticket.shop_response is not None:
                    context['error_message'] = "Shop Response is already there for ticket."
                    return self.render_to_response(context)
                if not request.user.groups.filter(name='Administrator').exists():
                    return HttpResponse("Permission denied")
                else:
                    order_ticket.shop_response = response
                    order_ticket.shop_reason = reason
                    order_ticket.shop_admin_support_reason = admin_support_reason
                    order_ticket.shop_response_time = timezone.now()

                    if response == 'COMPLETED':
                        complete(order_ticket.server_order)
                        order_ticket.status = COMPLETED
                        order_ticket.save()

            elif request.user.profile.server == server_order.server:
                if order_ticket.server_response is not None:
                    context['error_message'] = "Server Response is already there for ticket."
                    return self.render_to_response(context)
                else:
                    order_ticket.server_response = response
                    order_ticket.server_reason = reason
                    order_ticket.server_admin_support_reason = admin_support_reason
                    order_ticket.server_response_time = timezone.now()

                    if response == CANCELLED:
                        cancel(order_ticket.server_order)
                        order_ticket.status = COMPLETED
                        order_ticket.save()

            elif request.user.is_staff or request.user.is_superuser:
                print "request user is staff",request.user.is_staff
                print "request user is admin",request.user.is_superuser
                print "request user name",request.user.username
                if order_ticket.status != ADMIN_SUPPORT:
                    context['error_message'] = "Ticket not valid for admin response"
                    return self.render_to_response(context)
                if order_ticket.admin_response is not None:
                    context['error_message'] = "Admin Response is already there for ticket."
                    return self.render_to_response(context)
                AdminActionHistory.objects.create(action="Admin responded to ticket #"+str(order_ticket.id), user=request.user, affected="Ticket")
                order_ticket.admin_response = response
                order_ticket.admin_reason = reason
                order_ticket.admin_response_time = timezone.now()

            else:
                context['error_message'] = "Not Authorized to respond for ticket."
                return self.render_to_response(context)
            order_ticket = utils.validate_and_update_ticket(order_ticket)
            if order_ticket is None:
                context['error_message'] = "Some error occurred in receiving response for ticket"
                return self.render_to_response(context)
            else:
                context['ticket'] = order_ticket
                context['success_message'] = "Your response has been received for the ticket."
                return redirect(reverse('ticket_detail',kwargs={'pk': order_ticket.id}))
        # for receiving server comments on the ticket.
        elif action == 'server_comments':
            if order_ticket.server_comments is not None:
                context['error_message'] = "Server Comments are already there for ticket."
                return self.render_to_response(context)
            if 'server_comments' in request.POST:
                server_comments = request.POST.get('server_comments')
            else:
                context['error_message'] = "No Server Comments are given for the ticket."
                return self.render_to_response(context)
            server_files = None
            print "request.Files: ", request.FILES
            if 'server_files' in request.FILES:
                server_files = request.FILES.getlist('server_files')
                for server_file in server_files:
                    print server_file
                    print server_file.name

            print "server_files: ", server_files
            order_ticket.server_comments = server_comments
            order_ticket.server_comments_time = timezone.now()
            if server_files is not None:
                for server_file in server_files:
                    print server_file
                    file_ext = server_file.name.split(".")[-1].lower()
                    new_file = FileUpload.objects.create(actual_file_name=server_file.name, uploaded_file=server_file,
                                                         file_extension_name=file_ext)
                    order_ticket.server_files.add(new_file)
            order_ticket.save()
            context['ticket'] = order_ticket
            context['success_message'] = "Your comments has been received for the ticket."
            return redirect(reverse('ticket_detail',kwargs={'pk': order_ticket.id }))
        return self.render_to_response(context)


@login_required
@csrf_exempt
@transaction.atomic
def create_message(request, ticket_id):
    print 'create_message for ticket_id: ', ticket_id
    try:
        if request.method == 'POST':
            message_text = request.POST.get('message')
            user = request.user
            response = {}
            try:
                order_ticket = OrderTicket.objects.get(id=ticket_id)
            except Exception, e:
                response['error_message'] = "Order Ticket Not Found for id ", ticket_id
                response['error'] = True
                return JsonResponse(response)
            server_order = order_ticket.server_order
            current_user_shop = request.user.profile.shop
            current_user_server = request.user.profile.server
            sender = None
            if user.is_superuser or user.is_staff:
                sender = user
            elif current_user_shop is not None:
                if current_user_shop == server_order.shop:
                    sender = user
            elif current_user_server is not None:
                if current_user_server == server_order.server:
                    sender = user

            if sender is None:
                response['error_message'] = "invalid user to send the message"
                response['error'] = True
                return JsonResponse(response)
            message_file = None
            if 'message_file' in request.FILES:
                    message_file = request.FILES.get('message_file')
            try:
                message = utils.create_message(order_ticket, sender, message_text, message_file)
                if message is None:
                    response['error_message'] = "Error While Sending Message"
                    response['error'] = True
                else:
                    response['success'] = True
                    response['message_text'] = message.message_text
                    response['created_at'] = message.created_at.strftime("%b. %d %Y, %I:%M %p")
                    if message.sender.first_name is not None and message.sender.first_name != '':
                        response['sender_name'] = message.sender.first_name
                    else:
                        response['sender_name'] = 'N.A.'
                    message_files = message.message_files.all()
                    if len(message_files)>0:
                        message_file = message_files[0]
                        print message_file
                        response['file_url'] = message_file.uploaded_file.url
                        response['file_name'] = message_file.actual_file_name
            except Exception,e:
                print e
                response['error_message'] = "Some error Occurred"
                response['error'] = True
            return JsonResponse(response)
    except Exception, e:
        print e
    return Http404





# @login_required
# @csrf_exempt
# def ticket_response(request, ticket_id):
#     if request.method == 'GET' and request.GET.get('id', None) is not None:
#         response = request.GET.get('response')
#         user = request.user
#         response = {}
#         try:
#             order_ticket = OrderTicket.objects.get(id=ticket_id)
#         except Exception, e:
#             response['error_message'] = "Order Ticket Not Found for id ", ticket_id
#             response['error'] = True
#             return JsonResponse(response)
#         server_order = order_ticket.server_order
#         shop_user = server_order.shop.user_shop.user
#         server_user = server_order.server.user_server.user
#         sender = user
#         if sender == server_user:
#             order_ticket.server_response = response
#             order_ticket.server_response_time = timezone.now()
#         elif sender == shop_user:
#             order_ticket.shop_response = response
#             order_ticket.shop_response_time = timezone.now()
#         else:
#             response['error_message'] = "Invalid Recipient"
#             response['error'] = True
#             return JsonResponse(response)
#         try:
#             order_ticket.save()
#         except Exception,e:
#             print e
#             response['error_message'] = "Some error occurred in updating response for ticket"
#             response['error'] = True
#         return JsonResponse(response)
#     return Http404
