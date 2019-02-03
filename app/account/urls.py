# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import patterns, url

from .views import (ProfileView, ChangeEmailView, CreateUserView, DeleteUserView,BlockUserView,
                    EmailConfirmationView, AccountActivationView, LoginView, UserView, AddUserView, CreateBusinessView, RedirectUserToBusinessView)
from .forms import ResetPasswordForm, ChangePasswordForm
urlpatterns = patterns('',

                       # Account creation and confirmation
                       url(r'^$', RedirectUserToBusinessView.as_view(), name='user-business'),
                       url(r'^create/$',
                           CreateUserView.as_view(),
                           name='create_account'),
                       url(r'^create/done/$',
                           EmailConfirmationView.as_view(),
                           name='email_confirmation'),
                       url(r'^confirm-email/(?P<confirmation_key>\w+)/$',
                           ChangeEmailView.as_view(),
                           name='change_email'),
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           AccountActivationView.as_view(),
                           name='account_activation'),
                       # User profile
                       url(r'^profile/$', ProfileView.as_view(),
                           name='profile'),
                       # reset and change password
                       url(r'^password/reset/$', 'django.contrib.auth.views.password_reset',
                           {'template_name': 'urpsm/accounts/password_reset.html',
                            'password_reset_form': ResetPasswordForm,
                            #'email_template_name': 'urpsm/email/password_reset_email.txt'
                            },
                           name='password_reset'),

                       url(r'^password/reset/done/$',
                           'django.contrib.auth.views.password_reset_done',
                           {'template_name':
                               'urpsm/accounts/v2/password_reset_done.html'},
                           name='password_reset_done'),

                       url(r'^password/change/$', 'django.contrib.auth.views.password_change',
                           {'template_name':
                               'urpsm/v2/accounts/password_change.html',
                               'password_change_form': ChangePasswordForm,
                            },
                           name='password_change'),

                       url(r'^password/change/done/$',
                           'django.contrib.auth.views.password_change_done',
                           {'template_name':
                               'urpsm/accounts/password_change_done.html'},
                           name='password_change_done'),

                       url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           'django.contrib.auth.views.password_reset_confirm',
                           {
                               'template_name': 'urpsm/accounts/password_reset_confirm.html',
                           },
                           name="password_reset_confirm"),


                       url(r'^reset/done/$',
                           'django.contrib.auth.views.password_reset_complete',
                           {'template_name':
                               'urpsm/accounts/password_reset_complete.html'},
                           name="password_reset_complete"),

                       # Login
                       # url(r'^login/$', 'django.contrib.auth.views.login',
                       #     {
                       #         'template_name': 'urpsm/accounts/login_form.html',
                       #         'authentication_form': LoginForm
                       #     },
                       #     name='login'),

                       url('^login/$', LoginView.as_view(), name="login"),

                       # logout
                       url(r'^logout/$', 'django.contrib.auth.views.logout',
                           {
                               'template_name': 'urpsm/accounts/logout.html',
                               'next_page': '/',
                           },
                           name='logout'),

                       # frontend urls
                       url(r'^users/$', UserView.as_view(), name="users"),
                       url(r'^user/add/$', AddUserView.as_view(), name="user-add"),
                       url(r'^(?P<pk>\d+)/delete/$',
                           DeleteUserView.as_view(), name='user-delete'),
                       url(r'^(?P<pk>\d+)/block/$',
                           BlockUserView.as_view(), name='user-block'),

                       url(r'^create-business', CreateBusinessView.as_view(), name='create-business')
                       
                       )
