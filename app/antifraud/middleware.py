
# from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import HttpResponseRedirect

# from django.contrib.sessions.models import Session
# from tracking.models import Visitor
# from datetime import datetime
from django.core.urlresolvers import resolve
from django.contrib.sessions.middleware import SessionMiddleware
from app.account.utils import get_client_ip
from mobilify.utils import PrintException

from django.conf import settings
from django.core.cache import cache, get_cache
from django.utils.importlib import import_module
from app.antifraud.utils import delete_user

# from security_session.middleware import SessionSecurityMiddleware




class LogoutMiddleware(object):
    def process_request(self, request):
        current_url = resolve(request.path_info).url_name
        try:
            if 'logout' in current_url:
                print request.user
                if request.user.profile.shop:
                    country = request.user.profile.shop.country.name
                if request.user.profile.server:
                    country = request.user.profile.server.country.name
                delete_user(request.user.email, country)
                cache_key = "user_pk_%s_restrict" % request.user.pk
                cache = get_cache('default')
                cache_value = cache.get(cache_key)
                engine = import_module(settings.SESSION_ENGINE)
                session = engine.SessionStore(session_key=cache_value)
                session.delete()
        except:
            pass


class UserRestrictMiddleware(object):
    def process_request(self, request):
        """
        Checks if different session exists for user and deletes it.
        """
        if request.user.is_authenticated():
            cache = get_cache('default')
            cache_timeout = 86400
            cache_key = "user_pk_%s_restrict" % request.user.pk
            cache_value = cache.get(cache_key)

            if cache_value is not None:
                if request.session.session_key != cache_value:
                    engine = import_module(settings.SESSION_ENGINE)
                    session = engine.SessionStore(session_key=cache_value)
                    session.delete()
                    cache.set(cache_key, request.session.session_key, 
                              cache_timeout)
            else:
                cache.set(cache_key, request.session.session_key, cache_timeout)

class SessionRestrictMiddleware(SessionMiddleware):
    def process_request(self, request):
        try:
            ip_address = get_client_ip(request)
            if request.method == 'POST' and not request.is_ajax():
                print request.user.profile.ip_address, ip_address, "XXXXXXXXXXXX"
                if request.user.profile.ip_address:
                    if not request.user.profile.ip_address == ip_address:
                        return HttpResponseRedirect(reverse_lazy('error-404'))
                    else:
                        return HttpResponseRedirect(reverse_lazy('error-404'))
        except:
            PrintException()

        # super(SessionRestrictMiddleware, self).process_request(request)




# class SessionRestrictMiddleware(object):
#     """
#     Prevents more than one user logging in at once from two different IPs
#     """
#     def process_request(self, request):
#         try:
#             current_url = resolve(request.path_info).url_name
#             if 'login' in current_url and not request.is_ajax():
#                 ip_address = request.META.get('REMOTE_ADDR','')
#                 browser = request.META.get('HTTP_USER_AGENT','')
#                 print ip_address
#                 try:
#                     last_login = request.user.last_login
#                 except:
#                     last_login = None
#                 if last_login:
#                     if Visitor.objects.filter(ip_address=ip_address).exists():
#                         last = Visitor.objects.filter(ip_address=ip_address, end_time=False).last()
#                         if request.user.username == last.user.username:
#                             return HttpResponseRedirect(reverse_lazy('error-404'))
#         except:
#             pass
#                 # previous_visitors = Visitor.objects.filter(user=request.user.pk)
#                 # for visitor in previous_visitors:
#                 #     Session.objects.filter(session_key=visitor.session_key).delete()
#                 #     print visitor
#                 #     visitor.user = None
#                 #     visitor.save()




class NoDuplicateSessionMiddleware(object):

    def process_request(self, request):
            ip =  get_client_ip(request)
            if ip and request.user.is_authenticated():
                username = request.user.username
                if request.user.profile.shop:
                    business = request.user.profile.shop
                elif request.user.profile.server:
                    business = request.user.profile.server
                country = business.country
                
                user_info = "%s %s %s\n" % (ip, username, business)
                if not check_user(user_info, country):
                    print record_user(user_info, country), 'record'
                else:
                    return HttpResponseRedirect(reverse_lazy('error-404'))
            else:
                print ip