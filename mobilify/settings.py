# -*- coding: utf-8 -*-
"""
Django settings for mobilify project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
from __future__ import absolute_import

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y1y&a1&s31mwtjs09d!1x0g*f0v3^x+e5zav52yzu@gemz22xd'

# SECURITY WARNING: don't run with debug turned on in production!

if 'hamza\\mob' in BASE_DIR:
    from .dev import *
else:
    from .production import *

# Application definition
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

SITE_ID = 1

ALLOW_UNICODE_SLUGS = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.*', '0.0.0.0', '.urpsm.com']

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin.apps.SimpleAdminConfig',
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    # 'django.contrib.gis',


    'suit_redactor',
    'app.account',
    'app.client',
    'app.component',
    'app.dash',
    'app.order',
    'app.phone',
    'app.shop',
    'app.endpoint',
    'app.server',
    'app.ureview',
    'app.public',
    'app.launch',
    'app.ticket',
    'app.payment',
    'app.notifications',
    'app.antifraud',
    'app.search',

    'paypal.standard.ipn',
    'braces',
    'django_countries',
    'django_extensions',
    'django_select2',
    'easy_thumbnails',
    'location_field',
    'smart_selects',
    'simplecities',
    'social.apps.django_app.default',
    'el_pagination',
    # 'whoosh',
    # 'haystack',
    'currencies',
    'session_security',
    # 'tracking',
    'django_otp',
    'django_otp.plugins.otp_static',
    'django_otp.plugins.otp_totp',
    'two_factor',
    'versatileimagefield',
     # "django_hstore",

)

if DEBUG and not '/home/' in BASE_DIR:
    INSTALLED_APPS += ('debug_toolbar', )

MIDDLEWARE_CLASSES = (
    # 'tracking.middleware.VisitorTrackingMiddleware',
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'app.antifraud.middleware.UserRestrictMiddleware',
    # 'app.antifraud.middleware.LogoutMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'session_security.middleware.SessionSecurityMiddleware',
    'two_factor.middleware.threadlocals.ThreadLocals',
)

ROOT_URLCONF = 'mobilify.urls'

WSGI_APPLICATION = 'mobilify.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                "django.core.context_processors.request",
                'django.core.context_processors.media',
                'app.shop.context_processors.adverts',
                'mobilify.context_processors.googlemap_key',
                'social.apps.django_app.context_processors.backends',
                # 'social.apps.django_app.context_processors.login_redirect',
                'app.account.context_processors.css_direction',
                ],
            },
        },

    # {
    #     'BACKEND': 'django.template.backends.jinja2.Jinja2',
    #     'DIRS': [
    #         os.path.join(BASE_DIR, 'templates/jinja2'),
    #         # os.path.join(BASE_DIR, 'templates_v2/jinja2'),
    #         ],
    #     'APP_DIRS': True,
    #     'OPTIONS': {
    #         'environment': 'mobilify.jj.environment',
    #         'extensions': [
    #             # 'jinja2.ext.i18n',
    #             'jinja2.ext.autoescape',
    #             ]
    #         },

    #     },

    ]

# if not DEBUG:
#     STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# if DEBUG:
#     STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# STATIC_URL = '/static/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# MEDIA_URL = '/media/'

AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
        'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
        'Cache-Control': 'max-age=94608000',
    }



# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
# STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

STATICFILES_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)
STATICFILES_STORAGE = 'mobilify.custom_storages.StaticStorage'

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'mobilify.custom_storages.MediaStorage'

# Suit settings
from .suit import *

# Easy thumbnails aliases
THUMBNAIL_ALIASES = {
    '': {
        'small':     {'size':   (32, 32), 'crop': False},
        'thumbnail': {'size':   (64, 64), 'crop': False},
        'shop':      {'size': (120, 120), 'crop': False},
        'server':    {'size': (120, 120), 'crop': False},
        'brand':     {'size': (180, 150), 'crop': False},
        'model':     {'size': (160, 200), 'crop': False},
        'advert':    {'size': (180, 150), 'crop': False},
        'medium':    {'size': (300, 300), 'crop': False},
        'large':     {'size': (640, 640), 'crop': False},
        },
    }

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'defaults': [
        ('list_view', 'crop__100x100'),
        ('dashboard', 'crop__400x400'),
        # ('product_page_mobile', 'crop__680x680'),
        # ('product_page_big', 'crop__750x750'),
        # ('product_page_thumb', 'crop__280x280')
        ]
        }

VERSATILEIMAGEFIELD_SETTINGS = {
    # Images should be pre-generated on Production environment
    'create_images_on_demand': True, #os.environ.get('CREATE_IMAGES_ON_DEMAND'),
}


DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'app.account.backend.MBackend',
    'django.contrib.auth.backends.ModelBackend',

    )
# if "/home/" in BASE_DIR:
#     FACEBOOK_APP_ID             = '723072354462659'
#     FACEBOOK_APP_SECRET         = '3f3eb145f47b1a60290610bd0278d1cc'
#     GOOGLE_OAUTH2_CLIENT_ID     = "325265354341-nvcbq5nds9u07p6p0uot8i86mkakf5tb.apps.googleusercontent.com"
#     GOOGLE_OAUTH2_CLIENT_SECRET = "iyHx2_BPQp-fQft-8Tmb9Ozj"
# else:
#     from .dev import FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, GOOGLE_OAUTH2_CLIENT_ID, GOOGLE_OAUTH2_CLIENT_SECRET

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 60 * 60

#social auth settings
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY    = GOOGLE_OAUTH2_CLIENT_ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_OAUTH2_CLIENT_SECRET
SOCIAL_AUTH_FACEBOOK_KEY         = FACEBOOK_APP_ID
SOCIAL_AUTH_FACEBOOK_SECRET      = FACEBOOK_APP_SECRET
SOCIAL_AUTH_FACEBOOK_SCOPE       = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = { 'fields': 'id,name,email', }

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_by_email',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    # 'app.account.pipeline.is_shop_or_server_owner',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'app.account.pipeline.get_user_email',
    'app.account.pipeline.add_user_group',
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social.pipeline.disconnect.allowed_to_disconnect',
    'social.pipeline.disconnect.get_entries',
    'social.pipeline.disconnect.revoke_tokens',
    'social.pipeline.disconnect.disconnect',
)
# NORECAPTCHA_SITE_KEY = '6Lf7GswSAAAAAFEGqon9M-TG9ZzdqMaPE8pXfrzl'
# NORECAPTCHA_SECRET_KEY = '6Lf7GswSAAAAAB-B0z_wKgt8nQXaLZymzYGGMb52'

LOCALE_PATHS =  os.path.join(BASE_DIR, 'locale'),

LANGUAGES = (
    ('fr', 'Français'),
    ('ar', 'العربية'),
    ('en', 'English'),
    # ('es', 'Spanish'),
    # ('pt-br', 'Portuguese'),
)
#django-localeurl-end
LOCALEURL_USE_ACCEPT_LANGUAGE  = True
LOCALEURL_USE_SESSION   = True

# if not 'hamza\mob' in BASE_DIR:
GOOGLE_MAP_KEY = 'AIzaSyBKm8aAAWjp4PSS7ej9Fep5AjXzBJhitnk'

EL_PAGINATION_PER_PAGE = 10


#Search engine


# if not "d:" in BASE_DIR:
    # SSLIFY_DISABLE =  False

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_SECURITY_WARN_AFTER = 3480

SESSION_SECURITY_EXPIRE_AFTER = 3580



TWO_FACTOR_CALL_GATEWAY = 'mobilify.gateways.Messages'
TWO_FACTOR_SMS_GATEWAY = 'mobilify.gateways.Messages'
PHONENUMBER_DEFAULT_REGION = 'MA'

TWO_FACTOR_SMS_GATEWAY = 'two_factor.gateways.twilio.gateway.Twilio'
TWO_FACTOR_CALL_GATEWAY = 'two_factor.gateways.twilio.gateway.Twilio'
TWILIO_ACCOUNT_SID = 'AC4b9840e00de21408fdba356f6c0ae03b'
TWILIO_AUTH_TOKEN = 'a3cad764651b3f12a40dd5b84b0968fc'
TWILIO_CALLER_ID = '+16284000061'
# TWILIO_CALLER_ID = 'US71228b08693b938a3c25a0da68ac03bb'

from django.core.urlresolvers import reverse_lazy
LOGIN_URL = 'two_factor:login'

#EMAIL_BACKEND               = "sgbackend.SendGridBackend"


ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
SEARCHBOX_URL = os.environ.get('SEARCHBOX_URL')
BONSAI_URL = os.environ.get('BONSAI_URL')
# We'll support couple of elasticsearch add-ons, but finally we'll use single
# variable
ES_URL = ELASTICSEARCH_URL or SEARCHBOX_URL or BONSAI_URL or ''
if ES_URL:
    SEARCH_BACKENDS = {
        'default': {
            'BACKEND': 'app.search.backends.elasticsearch2',
            'URLS': [ES_URL],
            'INDEX': os.environ.get('ELASTICSEARCH_INDEX_NAME', 'urpsm'),
            'TIMEOUT': 15,
            'AUTO_UPDATE': True},
    }
else:
    SEARCH_BACKENDS = {}

PAGINATE_BY = 12

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}