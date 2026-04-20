from django import template

register = template.Library()

@register.filter
def faceit_icon(level):
    return f'images/faceit/lvl{level}.svg'
