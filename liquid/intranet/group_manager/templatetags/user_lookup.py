from django import template
from intranet.models import GroupMember
register = template.Library()

@register.filter
def pk_to_full_name(id):
	m = GroupMember.objects.get(pk=id)
	return m.member.full_name()

@register.filter
def pk_to_netid(id):
	m = GroupMember.objects.get(pk=id)
	return m.member.username

@register.filter
def pk_to_date_joined(id):
	m = GroupMember.objects.get(pk=id)
	return m.date_joined