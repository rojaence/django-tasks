from django import template

register = template.Library()


@register.simple_tag
def urlparams(*_, **kwargs):
    query = ''
    for key in kwargs.keys():
        query += f'{key}={kwargs[key]}&'
    return '?' + query[:-1] if query else ''
