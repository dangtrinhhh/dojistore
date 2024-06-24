from django import template
import urllib.parse

register = template.Library()

@register.filter
def fix_url(url):
    if 'https' in url:
        return url.replace('/media/https%3A', 'https:/')
    return url
