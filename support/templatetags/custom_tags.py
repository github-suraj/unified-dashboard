import re
from django import template

register = template.Library()


@register.filter(name='re_search')
def re_search(value, regex):
    return re.search(regex, value)


@register.filter(name='textarea_rows')
def textarea_rows(value):
    return value.split('\n').__len__() + 1
