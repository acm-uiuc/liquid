from django import template
from django.utils.functional import allow_lazy
from django.utils.safestring import mark_safe, SafeData, mark_for_escaping
from django.template.defaultfilters import stringfilter
from django.utils.html import (conditional_escape, escapejs, fix_ampersands,
    escape, urlize as urlize_impl, linebreaks, strip_tags)
import re
register = template.Library()


@register.filter("replacelinks", is_safe=True, needs_autoescape=True)
@stringfilter
def replacelinks(value, autoescape=None):
    autoescape = autoescape and not isinstance(value, SafeData)
    return mark_safe(links(value, autoescape))

def create_link(match):
   return "<a href='%s' target='_blank'>%s</a>"%(match.group(0),match.group(0))

def links(value, autoescape=False):
   link_reg = r'http[s]?://[^\s<>"]+|www\.[^\s<>"]+'
   if autoescape:
      text = re.sub(link_reg,create_link,escape(value))
   else:
      text = re.sub(link_reg,create_link,value)
   return text
