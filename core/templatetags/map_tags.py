from django import template
from core.models import Body

register = template.Library()


@register.simple_tag
def system_rows(system):
    return range(-system.size, system.size + 1)


@register.simple_tag
def system_cols(system, row):
    start = -system.size + max(-row, 0)
    stop = 1 + system.size - max(row, 0)
    return range(start, stop)


@register.simple_tag
def system_body(system, position_x, position_y):
    bodies = Body.objects.filter(system=system, x=position_x, y=position_y)
    return bodies.first()
