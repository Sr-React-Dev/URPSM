# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .models import Banner


def adverts(request):
    banners = Banner.objects.filter(active=True)
    context = {'banners': banners, }
    return context
