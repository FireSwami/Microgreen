from django import template
from green.models import *

register = template.Library()  # переменная регистр - ссылка на библиотеку

@register.simple_tag(name='getcats')  # превращает функцию в простой тэг
# задаем имя getcats, как синоним для функции
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)

@register.inclusion_tag('green/list_categories.html') # сложный тэг, возвращает
# фрагмент страницы html
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {"cats": cats, "cat_selected": cat_selected}


