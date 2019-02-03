"""
Production mode settings
"""
import dj_database_url, os, ast
# from .dev import HAYSTACK_CONNECTIONS
DEBUG = False
# TEMPLATE_DEBUG = DEBUG

DATABASES = dict()
DATABASES['default'] = dj_database_url.config(default=os.environ['DATABASE_URL'])
DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

SECRET_KEY                  = os.environ['SECRET_KEY']
FACEBOOK_APP_ID             = os.environ['FACEBOOK_APP_ID']
FACEBOOK_APP_SECRET         = os.environ['FACEBOOK_APP_SECRET']
FACEBOOK_APP_SECRET         = os.environ['FACEBOOK_APP_SECRET']
GOOGLE_OAUTH2_CLIENT_ID     = os.environ['GOOGLE_OAUTH2_CLIENT_ID']
GOOGLE_OAUTH2_CLIENT_SECRET = os.environ['GOOGLE_OAUTH2_CLIENT_SECRET']

AWS_ACCESS_KEY_ID           = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY       = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME     = 'urpsm-assets'
if os.environ.get('EMAILER') == 'sendgrid':
	EMAIL_BACKEND               = 'mailer.backend.DbBackend'
	EMAIL_HOST_USER             = os.environ['SENDGRID_USERNAME']
	EMAIL_HOST                  = 'smtp.sendgrid.net'
	EMAIL_PORT                  = 587
	EMAIL_USE_TLS               = True
	EMAIL_HOST_PASSWORD         = os.environ['SENDGRID_PASSWORD']
	EMAIL_BACKEND               = "sgbackend.SendGridBackend"
	SENDGRID_USER               = os.environ['SENDGRID_USERNAME']
	SENDGRID_PASSWORD           = os.environ['SENDGRID_PASSWORD']
	SENDGRID_API_KEY            = os.environ['SENDGRID_API_KEY']
	EMAIL_PASSWORD              = EMAIL_HOST_PASSWORD
elif os.environ.get('EMAILER') == 'zoho':
	SERVER_MAIL = os.environ.get('DEFAULT_FROM_EMAIL')
	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	EMAIL_USE_TLS = True
	EMAIL_HOST = 'smtp.zoho.com'
	EMAIL_PORT = 465
	EMAIL_HOST_USER = os.environ.get('DEFAULT_FROM_EMAIL')
	EMAIL_HOST_PASSWORD = EMAIL_PASSWORD = os.environ.get('DEFAULT_FROM_EMAIL_PASSWORD')

# Paypal settings
PAYPAL_RECEIVER_EMAIL       = os.environ.get('PAYPAL_RECEIVER_EMAIL')
PAYPAL_ADAPTIVE_PAYMENT_URL = os.environ.get('PAYPAL_ADAPTIVE_PAYMENT_URL')
PAYPAL_SENDER_EMAIL         = os.environ.get('PAYPAL_SENDER_EMAIL')
PAYPAL_CANCEL_URL           = os.environ.get('PAYPAL_CANCEL_URL')
PAYPAL_RETURN_URL           = os.environ.get('PAYPAL_RETURN_URL')

a = os.environ.get('X_PAYPAL_SECURITY_USERID')
b = os.environ.get('X_PAYPAL_SECURITY_PASSWORD')
c = os.environ.get('X_PAYPAL_SECURITY_SIGNATURE')
d = os.environ.get('X_PAYPAL_APPLICATION_ID')
e = os.environ.get('X_PAYPAL_REQUEST_DATA_FORMAT')
f = os.environ.get('X_PAYPAL_RESPONSE_DATA_FORMAT')
request_headers = {
    "X-PAYPAL-SECURITY-USERID": a,
    "X-PAYPAL-SECURITY-PASSWORD":  b,
    "X-PAYPAL-SECURITY-SIGNATURE":  c ,
    "X-PAYPAL-APPLICATION-ID":   d    ,
    "X-PAYPAL-REQUEST-DATA-FORMAT":e ,
    "X-PAYPAL-RESPONSE-DATA-FORMAT": f ,
}








