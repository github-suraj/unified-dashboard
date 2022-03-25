import re
from django import template

register = template.Library()

@register.filter(name='re_search')
def re_search(value, regex):
    return re.search(regex, value)
