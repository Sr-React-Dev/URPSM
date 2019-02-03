from __future__ import unicode_literals
from django.apps import AppConfig


class ProfileConfig(AppConfig):
    name = "app.account"
    verbose_name = 'User Profiles'

    def ready(self):
        from . import signals
