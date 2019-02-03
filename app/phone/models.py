from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from versatileimagefield.fields import VersatileImageField
# from smart_selects.db_fields import ChainedForeignKey
from slugify import slugify



class Brand(models.Model):
    logo = VersatileImageField(upload_to='brand/', blank=True, null=True)
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(editable=False, db_index=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        from app.notifications.models import Notification
        try:
            if not Notification.objects.filter(brand=self.obj).exists():
                Notification(brand=self, notification_type=Notification.NEW_BRAND_ADDED)
        except:pass
        super(Brand, self).save(*args, **kwargs)

  



class Model(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(editable=False, db_index=True)
    brand = models.ForeignKey(Brand, related_name='brand_models')
    picture = VersatileImageField(upload_to='phone/', blank=True, null=True, default='icons/default_phone.png')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    repairing_request = models.PositiveIntegerField(default=0)
    repaired_items    = models.PositiveIntegerField(default=0)

    unlocking_request = models.PositiveIntegerField(default=0)
    unlocked_items    = models.PositiveIntegerField(default=0)

    repairing_request = models.PositiveIntegerField(default=0)
    repaired_items    = models.PositiveIntegerField(default=0)

    # unlocking_request = models.PositiveIntegerField(default=0)
    # unlocked_items    = models.PositiveIntegerField(default=0)

    flashing_request = models.PositiveIntegerField(default=0)
    flashed_items    = models.PositiveIntegerField(default=0)

    satisfied_clients_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return unicode(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        notify = kwargs.get('notify', None)
        if notify:
            if not Notification.objects.filter(model=self, notification_type=Notification.NEW_MODEL_ADDED).exists():
                Notification(model=self, brand=self.brand, notification_type=Notification.NEW_MODEL_ADDED)
        super(Model, self).save(*args, **kwargs)

    class Meta:
        unique_together = (("name", "brand"),)

    # @property 
    # def repaired_phones_by_model_count(self):
    #     return self.client_model.filter(deleted=False, todo='r', paid=True, status='r').count()

    # @property 
    # def repaired_phones_by_model(self):
    #     return self.client_model.filter(deleted=False, todo='r', paid=True, status='r')



# class Picture(models.Model):

#     """
#     Description: Phone picture
#     """
#     brand = models.ForeignKey(Brand)
#     model = ChainedForeignKey(Model,
#                               chained_field='brand',
#                               chained_model_field='brand',
#                               show_all=False, auto_choose=True)
#     picture = models.ImageField(upload_to='phone/')

#     def __str__(self):
#         return unicode(self.model)
