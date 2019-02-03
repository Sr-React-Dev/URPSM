# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.contrib.auth.models import UserManager, User

from django.utils.six import text_type
from django.utils.encoding import smart_text
from .utils import get_key


class ProfileManager(UserManager):

    def create_user(self, username, email, password):

        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()

        profile = self.create_profile(new_user)
        profile.activation_email()

        return new_user

    def create_profile(self, user):

        if isinstance(user.username, text_type):
            user.username = smart_text(user.username)
        activation_key = get_key()
        profile = self.create(user=user, activation_key=activation_key)
        return profile

    def activate_user(self, activation_key):

        try:
            profile = self.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            return False

        user = profile.user
        user.is_active = True
        profile.save(using=self._db)
        user.save(using=self._db)
        return user
