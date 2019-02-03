from __future__ import absolute_import
from django.contrib.auth.models import User
from app.account.models import Profile
from app.antifraud.utils import check_user, record_user

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class MBackend(object):

    def authenticate(self, username=None, password=None, errors=[]):
        try:
            user = User.objects.get(username=username)
            if user.is_superuser:
                return user
            profile = Profile.objects.get(user=user)
            
            # if profile.shop:
            #     country = profile.shop.country.name
            # if profile.server:
            #     country = profile.server.country.name

            # already_logged_in = check_user(user.email, country)

            # if already_logged_in:
            #     raise ValidationError(_('This account is already opened.'))
            #     return AnonymousUser()
            # else:
            #     record_user(user.email, country)


            if profile.shop is None:
                if not profile.block_access and user.check_password(password):
                    return user
                else:
                    # errors.append('Your account has been blocked')
                    return None
            if profile.server is None:
                if not profile.block_access and user.check_password(password):
                    return user
                else:
                    # errors.append('Your account has been blocked')
                    return None
            else:
                if not profile.block_access and not profile.shop.blocked and user.check_password(password):
                    return user
                else:
                    # errors.append('Your account has been blocked')
                    return None

        except User.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
