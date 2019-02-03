from social.exceptions import AuthAlreadyAssociated, AuthException, \
                              AuthForbidden

from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User, Group

from social.pipeline.partial import partial


@partial
def require_email(strategy, details, user=None, is_new=False, *args, **kwargs):
    if kwargs.get('ajax') or user and user.email:
        return
    elif is_new and not details.get('email'):
        email = strategy.request_data().get('email')
        if email:
            details['email'] = email
        else:
            return redirect('require_email')



@partial
def is_shop_or_server_owner(strategy, details, user=None, is_new=False, *args, **kwargs):
    print 'is_shop_or_server_owner:',user
    if user:
        _user = User.objects.get(username=user)
        print _user
        if _user.profile.block_access:
            return redirect(reverse_lazy('error-404'))
        if _user.profile.shop:
            if   _user.profile.shop.blocked:
                return redirect(reverse_lazy('error-404'))
            else:
                return redirect(reverse_lazy('shop-position'))
        elif _user.profile.server:
            if  _user.profile.server.blocked:
                return redirect(reverse_lazy('error-404'))
            else:
                return redirect(reverse_lazy('server-position'))
        elif not _user.profile.phone:
            return redirect(reverse_lazy('profile')) 
        else:
            return redirect(reverse_lazy('create-business'))


    return kwargs


def is_shop_or_server_owner_(strategy, details, user=None, *args, **kwargs):
    # print user
    # print details
    # print args, kwargs
    # username = user
    _user = User.objects.get(username=user)
    # print 'username', username

    if not _user.profile.block_access:
        try:
            kwargs['shop_blocked'] = _user.profile.shop.blocked 
        except:
            kwargs['shop_blocked'] = None

        try:
            kwargs['server_blocked'] = _user.profile.server.blocked 
        except:
            kwargs['server_blocked'] = None

        kwargs['block_access']  = False
        kwargs['user'] = _user
    else:
        kwargs['block_access']  = True
        
    # else:
        # errors.append('Your account has been blocked')
    return kwargs
    # try:
    #   pass
    # except User.DoesNotExist:
    #         return None

    # except AttributeError:
    #         return None

# def is_shop_owner():

def bifork(**kwargs):
    # if snot kwargs['block_access']:
    redirect(reverse_lazy('login'))

import json
import urllib2

def get_user_email(strategy, *args, **kwargs):
    if not kwargs['is_new']:
        return

    user = kwargs['user']
    if not user.email:

        fbuid = kwargs['response']['id']
        access_token = kwargs['response']['access_token']

        url = u'https://graph.facebook.com/{0}/' \
              u'?fields=email' \
              u'&access_token={1}'.format(
            fbuid,
            access_token,
        )

        request = urllib2.Request(url)
        email = json.loads(urllib2.urlopen(request).read()).get('email')

        user.email = email
        user.save()
    # return user
    return kwargs


def add_user_group(strategy, *args, **kwargs):
    user = kwargs['user']
    if user and not user.groups.filter(name='Administrator').exists():
        group, created = Group.objects.get_or_create(name='Administrator')
        user.groups.add(group)
        user.save()

    return kwargs