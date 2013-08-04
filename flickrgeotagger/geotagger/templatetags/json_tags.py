from django import template
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

from json import dumps

register = template.Library()


@register.filter
def json(var):
    return mark_safe(dumps(var, cls=DjangoJSONEncoder))
