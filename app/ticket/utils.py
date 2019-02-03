from django.utils import timezone
from django.db import transaction

from app.ticket.models import OrderTicket, TicketMessage, FileUpload, ADMIN_SUPPORT, COMPLETED, CANCELLED, INITIATED
from app.notifications.models import Notification



@transaction.atomic
def create_ticket_for_order(server_order, comments, shop_files):
    print "server order id: ", server_order.id
    ticket = OrderTicket(shop_comments=comments, server_order=server_order, created_at=timezone.now(),
                         shop_comments_time=timezone.now(), status=INITIATED)
    ticket.save()
    if shop_files is not None:
        print "Start saving files."
        for shop_file in shop_files:
            print shop_file
            file_ext = shop_file.name.split(".")[-1].lower()
            new_file = FileUpload.objects.create(actual_file_name=shop_file.name, uploaded_file=shop_file,
                                                 file_extension_name=file_ext)
            ticket.shop_files.add(new_file)
        ticket.save()
    Notification.objects.create(from_user=server_order.shop.user_shop.all()[0].user,
                                to_user=server_order.server.user_server.all()[0].user, server=server_order.server,
                                shop=server_order.shop, server_order=server_order,
                                notification_type=Notification.NEW_TICKET,
                                ticket=ticket)
    return ticket


@transaction.atomic
def create_message(order_ticket, sender, message_text, message_file):
    try:
        message = TicketMessage.objects.create(sender=sender, order_ticket=order_ticket, message_text=message_text)
        if message_file is not None:
            print message_file
            file_ext = message_file.name.split(".")[-1].lower()
            new_file = FileUpload.objects.create(actual_file_name=message_file.name, uploaded_file=message_file,
                                                 file_extension_name=file_ext)
            message.message_files.add(new_file)
            message.save()
        return message
    except Exception, e:
        print "Error Occurred While saving message from ", sender, " for ticket_id ", order_ticket.id, "with message ", message_text, " : ", e
        return None

@transaction.atomic
def validate_and_update_ticket(order_ticket):
    import app.order.utils as order_utils
    if order_ticket.status == INITIATED:
        if order_ticket.shop_response is not None and order_ticket.server_response is not None:
            if order_ticket.shop_response == order_ticket.server_response:
                print 'same shop and server respone'
                if order_ticket.shop_response == ADMIN_SUPPORT:
                    order_ticket.status = ADMIN_SUPPORT
                elif order_ticket.shop_response == COMPLETED:
                    if order_utils.complete_hold_server_order(order_ticket.server_order) is not None:
                        order_ticket.status = COMPLETED
                    else:
                        order_ticket = None
                elif order_ticket.shop_response == CANCELLED:
                    if order_utils.cancel_hold_server_order(order_ticket.server_order) is not None:
                        order_ticket.status = COMPLETED
                    else:
                        order_ticket = None
                else:
                    order_ticket = None
            else:
                print 'different shop and server respone'
                order_ticket.status = ADMIN_SUPPORT
    elif order_ticket.status == ADMIN_SUPPORT:
        if order_ticket.admin_response == COMPLETED:
            if order_utils.complete_hold_server_order(order_ticket.server_order) is not None:
                order_ticket.status = COMPLETED
            else:
                order_ticket = None
        elif order_ticket.admin_response == CANCELLED:
            if order_utils.cancel_hold_server_order(order_ticket.server_order) is not None:
                order_ticket.status = COMPLETED
            else:
                order_ticket = None
        else:
            order_ticket = None
    if order_ticket is not None:
        print "order ticket is not None : ", order_ticket
        order_ticket.save()
    else:
        print "order ticket is None : "
    return order_ticket


def get_message_file_name(uploaded_file, ref):
    import uuid

    file_ext = uploaded_file.name.split(".")[-1]
    print file_ext
    file_name = str(ref.id) + str(uuid.uuid4().hex[:6].upper()) + '.' + file_ext
    return file_name