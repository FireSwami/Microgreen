from django.core.cache import cache
from django.db.models import Count

from .models import *

menu = [{'title': "Карта сайта", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'}

        ]


class DataMixin:
    paginate_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs

        # кэширование  на низком уровне API

        cats = cache.get('cats')  # читаем колекцию cats по ключу cats из кэша
        if not cats:  # проверяем: если данные не были прочитаны, т.е. значение = None
            cats = Category.objects.annotate(Count('green'))  # то читаем БД
            cache.set('cats', cats, 60)  # и записываем в кэш на 60 сек

        user_menu = menu.copy()  # создаем копию словаря меню,
        if not self.request.user.is_authenticated:  # проверка на выполненный вход
            user_menu.pop(1)  # если не авторизован, то удаляется второй пункт из меню

        context['menu'] = user_menu  # передаем в контекст ссылку на измененное меню

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
