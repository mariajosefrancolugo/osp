from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.filter(name='last_first')
@stringfilter
def last_first(value):
    value = value.split(' ')
    value = value[1] + ', ' + value[0]
    return value
