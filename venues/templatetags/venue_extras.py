from django import template

register = template.Library()

@register.filter
def stars(rating):
    try:
        rating = int(rating)
    except (TypeError, ValueError):
        return ''
    return '★' * rating + '☆' * (5 - rating)