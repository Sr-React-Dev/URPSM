from django.contrib.auth.models import User
from app.shop.models import Shop
from app.server.models import Server
from app.order.models import ServerOrder, ShopOrder
from app.client.models import Client

from django.contrib.contenttypes.models import ContentType
from django.db.models import Model, ForeignKey, PositiveIntegerField, TextField, CharField, DateTimeField, FloatField
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils import timezone



class BaseReview(Model):

    user = ForeignKey( User,
        verbose_name=_('User'),
        blank=True, null=True,
    )

    content = TextField(
        max_length=1024,
        verbose_name=_('Content'),
        blank=True,
    )


    language = CharField(
        max_length=10,
        verbose_name=_('Language'),
        blank=True,
    )

    creation_date = DateTimeField(
        # auto_now_add=True,
        verbose_name=_('Creation date'),
        default= timezone.now
    )

    rating = FloatField(
        verbose_name=_('rating'),
        default=0,
    )
    class Meta:
        abstract = True
        ordering = ['-creation_date']



    def get_user(self):
        """Returns the user who wrote this review or ``Anonymous``."""
        if self.user:
            return self.user.email
        return ugettext('Anonymous')

class ShopReview(BaseReview):
    shop = ForeignKey(Shop, default=False,  related_name='review_shop')
    client = ForeignKey(Client, default=False, related_name='client_review')
    def __str__(self):
        return '{0} - {1}'.format(self.shop, self.get_user())

    def get_user(self):
        """Returns the user who wrote this review or ``Anonymous``."""
        if self.user:
            return self.user.username
        return ugettext('Anonymous')

class ServerReview(BaseReview):
    server = ForeignKey(Server, default=False, related_name='review_server')
    shop   = ForeignKey(Shop, default=False, related_name='shop_review')
    def __str__(self):
        return '{0} - {1}'.format(self.server.name, self.get_user())


class OrderReview(BaseReview):
    order  = ForeignKey(ServerOrder, blank=True, null=True)
    server   = ForeignKey(Server, blank=True, null=True)

    class Meta:
        verbose_name = _("reviewed order")
        verbose_name_plural = _("reviewed orders")

    def __str__(self):
        return _('Order #{0} by {1}').format(self.order, self.shop.name)




    # # content_type = ForeignKey(ContentType, null=True, default=False, blank=True)
    # object_id =PositiveIntegerField(null=True, default=False, blank=True)
    # reviewed_item = PositiveIntegerField(null=True, default=False, blank=True)
