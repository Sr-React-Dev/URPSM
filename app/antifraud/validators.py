from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _



def luhn_checksum(imei):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(imei)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def validate_imei(imei):
    valid = luhn_checksum(imei) == 0
    if not valid:
    	raise ValidationError(_('This is not a valid imei'))