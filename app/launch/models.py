from django.db import models

import datetime

class LaunchRock(models.Model):
    username       = models.CharField(max_length=255, default='user',blank=True, null=True)
    email      = models.EmailField()
    sign_date  = models.DateTimeField(default=datetime.datetime.now)
    ip         = models.GenericIPAddressField()
    http_refer = models.TextField(blank=True, null=True)
    message    = models.TextField(blank=True, null=True)
    notify_him = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.email
