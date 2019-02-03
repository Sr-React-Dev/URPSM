# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import phonenumber_field.modelfields
import app.account.managers


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(related_name='profile', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(help_text='eg: +212612345678', max_length=128, null=True, blank=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('activation_key', models.CharField(max_length=64, verbose_name='Activation key', blank=True)),
                ('unconfirmed_email', models.EmailField(max_length=254, verbose_name='Unconfirmed email', blank=True)),
                ('email_confirmation_key', models.CharField(max_length=64, verbose_name='New email verification key', blank=True)),
                ('shop', models.ForeignKey(related_name='user_shop', blank=True, to='shop.Shop', null=True)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
            managers=[
                ('objects', app.account.managers.ProfileManager()),
            ],
        ),
    ]
