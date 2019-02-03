from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
import logging
from . import models
# from .utils import get_client_ip
from mobilify.utils import PrintException
from app.antifraud.utils import get_client_ip, delete_user

logger = logging.getLogger("project")


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_handler(sender, instance, created, **kwargs):
    if not created:
        return
    # Create the profile object, only if it is newly created
    profile = models.Profile(user=instance)
    profile.save()
    logger.info('New user profile for {} created'.format(instance))


from django.contrib.auth.signals import user_logged_in, user_logged_out

@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
    # logger = logging.getLogger(__name__)
    # logger.info("user logged in: %s at %s" % (user, request.META['REMOTE_ADDR']))
    try:
        if  request.user.profile.ip_address is None:
            request.user.profile.ip_address = get_client_ip(request)
            request.user.profile.save()
    except:
        PrintException()


@receiver(user_logged_out)
def sig_user_logged_out(sender, user, request, **kwargs):
    # logger = logging.getLogger(__name__)
    # logger.info("user logged out: %s at %s" % (user, request.META['REMOTE_ADDR']))
    try:
        if request.user.profile.shop:
            country = request.user.profile.shop.country.name
        if request.user.profile.server:
            country = request.user.profile.server.country.name
            
        delete_user(request.user.email, country)

        if user.profile.ip_address == get_client_ip(request):
            user.profile.ip_address = None
            user.profile.save()
    except:
        PrintException()

