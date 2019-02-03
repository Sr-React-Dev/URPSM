# from django.contrib.gis.db import models


# class Waypoint(models.Model):

#     name = models.CharField(max_length=32)
#     geometry = models.PointField(srid=4326)
#     objects = models.GeoManager()

#     def __unicode__(self):
#         return '%s %s %s' % (self.name, self.geometry.x, self.geometry.y)

from django.db.models import CharField, EmailField, TextField, URLField, DateTimeField, Model, BooleanField

class Contact(Model):
    name        = CharField(max_length=50, default="John Doe", blank=False, null=False )
    subject     = CharField(max_length=255, default="Hello", blank=False, null=False )
    email       = EmailField(blank=False, null=False)
    website     = URLField(blank=True, null=True, default='')
    created_at  = DateTimeField(auto_now=True)
    message     = TextField(max_length=2048, blank=False, null=False)
    feedback    = TextField(max_length=2048, blank=True, null=True, default='')
    processed   = BooleanField(default=False)

    class Meta:
        verbose_name        = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return "{0}-{1}".format(self.subject, self.email)

