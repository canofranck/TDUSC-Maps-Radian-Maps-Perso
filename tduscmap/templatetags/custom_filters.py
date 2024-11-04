from django import template

register = template.Library()


@register.filter
def format_decimal(value):
    try:
        return "{:.2f}".format(float(value))
    except (TypeError, ValueError):
        return value
    
    
@register.filter
def to_percentage(value):
    try:
        return f"{float(value) * 100:.0f}%"
    except (TypeError, ValueError):
        return value