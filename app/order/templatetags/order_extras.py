from django.template.defaulttags import register
from django import template
import app.order.utils as order_utils
from app.ureview.models import OrderReview
from app.ureview.models import OrderReview

register = template.Library()

@register.filter
def is_order_valid_for_cancellation(server_order):
    return order_utils.validate_server_order_for_cancellation(server_order)

@register.filter
def is_order_not_rated(server_order):
    if server_order.status.upper() in ["REJECTED","IN PROCESS","PENDING"]:
        return False
    return not OrderReview.objects.filter(order=server_order).exists()

@register.filter
def get_order_rating(order):
    try:
        return OrderReview.objects.get(order=order).rating
    except Exception:
        return "-"

@register.filter
def halfrating(rating):
    return not rating%1==0


@register.filter
def status_color(status):
    color = "black"
    if status.lower() == "cancelled":
        color = "#ff9900"
    elif status.lower() == "pending":
        color = "#00ace6"
    elif status.lower() == "completed":
        color = "#00e6ac"
    return color

@register.filter
def status_color_class(status):
    d = "btn btn-sm"
    color = d+" btn-default"
    if status.lower() == "cancelled":
        color =d+ " btn-warning"
    elif status.lower() == "pending":
        color = d+" btn-primary"
    elif status.lower() == "completed":
        color = d+" btn-success"
    return color

@register.filter
def ticket_status_color(status):
    color = "#fc8675"
    if status == "ADMIN_SUPPORT":
        color = "#ff9900"
    elif status == "COMPLETED":
        color = "#00e6ac"
    return color

@register.filter
def get_order_rating(order):
    o = OrderReview.objects.filter(order=order)
    if o.count() > 0:
        return o[0].rating
    else:
        return 0

@register.filter
def shorten_service_name(name):
    return name[:50]