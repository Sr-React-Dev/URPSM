# -*- coding: utf-8 -*-
from django import template

register = template.Library()
 
from django.utils.translation import get_language, get_language_from_request
from datetime  import datetime
# from mobilify.settings import SWITCH_LANGUAGES
from django.core.urlresolvers import reverse


___ = lambda s: s

SWITCH_LANGUAGES =(
    ('ar', ___(u'العربية'), u'العربية'),
    ('en', ___(u'English'), 'En'),
    ('fr', ___(u'Français'), 'Fr'),
)

@register.inclusion_tag('urpsm/v2/public/tags/languages_dropdown_mobile_v2.html', takes_context=True)
def languages_dropdown_mobile(context, path):
    return language_dropdown(context, path)

@register.inclusion_tag('urpsm/v2/public/tags/languages_dropdown_desktop_v2.html', takes_context=True)
def languages_dropdown_desktop(context, path):
    return language_dropdown(context, path)

@register.inclusion_tag('urpsm/v2/dash/tags/languages_dropdown_dash_v2.html', takes_context=True)
def dash_languages_dropdown(context, path):
    return language_dropdown(context, path, True)

@register.filter
def pull( value , arg=False):
    '''
    
    '''
    
    if value =='ar':
        if arg:
            return 'pull-%s' % arg
        return 'pull-left'
    else:
        return 'pull-righ'

FLAGS = {'ar':'flags/sa.gif', 'fr':'flags/fr.gif', 'en':'flags/us.gif'}


def language_dropdown(context, path, flags=False):
    _current = current = None

    try:
        request = context['request']
        current = request.LANGUAGE_CODE
        # print current, 'CURRENT_LANGUAGE ?!?'
    except:
        current = get_language_from_request(request)
        # PrintException()
    if path == "/": 
        if current:
            _path='/%s/' % current
        else:
            _path = '/ar/'
            current = 'ar'
    else:
        _path=path
    languages = list()
    _langs    = {}
    for language in SWITCH_LANGUAGES:
        if not current == language[0]:
            bait = "/%s/" % current
            target = "/%s/" % language[0]

            if not path  == "/":
                new_path = _path.replace(bait, target)
                if flags:
                    flag = FLAGS[language[0]]
                    new_language = (language[1], new_path, False, flag)
                else:
                    new_language = (language[1], new_path, False)
            else:
                root = "%s/" % language[0]                
                new_language = (language[1], root, True)
                
            languages.append(new_language)
        else:
            _current = language[1]
        _langs[language[0]]=language[1]

    if not _current:
        _current = _langs[current]

    languages = tuple(languages)
    if flags:
        _current = FLAGS[current]

    return {'languages': languages, 'current':_current}


