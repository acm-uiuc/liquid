from django import template
register = template.Library()

@register.filter
def month_calendar(events):
    return "hi"