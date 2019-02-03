from django import template
from datetime import datetime
register = template.Library()

@register.filter
def concatenate(value, arg):
	return value % arg


@register.filter
def convert_to_date(value):
	try:
		return datetime.strptime(value, "%Y-%m-%d")
	except:
		return value
