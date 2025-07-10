from django import template
# store/templatetags/custom_filters.py

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return ''


@register.filter(name='currency')
def currency(value):
    return f"₹{value:.2f}"