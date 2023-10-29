"""Фильтры для шаблонов"""

from django import template

register = template.Library()


# добавление класса
@register.filter
def addclass(field, css):
    return field.as_widget(attrs={'class': css})
