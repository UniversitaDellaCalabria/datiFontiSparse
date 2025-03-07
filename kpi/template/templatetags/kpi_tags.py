from django import template
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone


register = template.Library()


@register.simple_tag
def year_list():
    return reversed(range(2020, timezone.localdate().year + 1))


@register.simple_tag
def settings_value(name, **kwargs):
    value = getattr(settings, name, None)
    if value and kwargs:
        return value.format(**kwargs)
    return value


@register.simple_tag
def user_from_pk(user_id):
    if not user_id:
        return False
    user_model = get_user_model()
    user = user_model.objects.get(pk=user_id)
    if not user:
        return False
    return user


@register.filter(name='split')
def split(value, key):
    if not value: return []
    return value.split(key)
