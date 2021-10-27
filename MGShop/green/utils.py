from django.core.cache import cache
from django.db.models import Count

from .models import Category

menu = [{'title': "Карта сайта", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'}

        ]


class DataMixin:
    paginate_by = 4

    def get_user_context(self, **kwargs):
        context = kwargs

        # кэширование  на низком уровне API

        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('green'))
            cache.set('cats', cats, 60)  # на 60сек

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
