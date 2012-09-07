from django import template
from intranet.models import Resume
register = template.Library()

@register.filter
def pk_to_created_at(id):
   r = Resume.objects.get(pk=id)
   return r.created_at

@register.filter
def pk_to_graduation(id):
   r = Resume.objects.get(pk=id)
   return r.person.graduation

@register.filter
def pk_to_seeking(id):
   r = Resume.objects.get(pk=id)
   return r.person.seeking

@register.filter
def pk_to_level(id):
   r = Resume.objects.get(pk=id)
   return r.person.level

@register.filter
def pk_to_name(id):
   r = Resume.objects.get(pk=id)
   return "%s %s"%(r.person.first_name,r.person.last_name)

@register.filter
def pk_to_thumb(id):
   r = Resume.objects.get(pk=id)
   return r.thumbnail_location
