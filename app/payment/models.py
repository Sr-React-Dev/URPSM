from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
# Create your models here.
from app.server.models import Server
from app.shop.models import Shop
from django.conf import settings


DEBIT = "DEBIT"
CREDIT = "CREDIT"

PAYMENT_TYPES = (
    (DEBIT, DEBIT),
    (CREDIT, CREDIT),
)


class BasePaymentTransaction(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, null=False)
    amount = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))],
                                 default=0, null=False)
    balance = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))],
                                  default=0, null=False)
    payment_type = models.CharField(max_length=100, null=False, choices=PAYMENT_TYPES)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(null=False)

    class Meta:
        abstract = True


class ServerPaymentTransaction(BasePaymentTransaction):
    server = models.ForeignKey(Server, null=False)

    def __str__(self):
        return self.description


class ShopPaymentTransaction(BasePaymentTransaction):
    shop = models.ForeignKey(Shop, null=False)

    def __str__(self):
        return self.description




