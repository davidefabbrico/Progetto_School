from django import template
from django.template.defaultfilters import register, stringfilter
# from django_email_verification import send_email

register = template.Library()

@register.filter(name='replaceUrl')
@stringfilter
def replaceUrl(value):
    return value.replace("92.222.9.65:8000", "progettoschool.it")