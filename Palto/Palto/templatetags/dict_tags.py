from django.template.defaulttags import register


@register.filter
def dict_get(d: dict, key: str):
    return d.get(key)
