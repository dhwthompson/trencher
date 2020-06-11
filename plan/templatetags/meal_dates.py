from django import template

from ..dates import date_name

register = template.Library()

register.filter(date_name)
