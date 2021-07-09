from django.contrib import admin
from django.forms import Textarea
from django.utils.safestring import mark_safe

from .models import *


class CreenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'get_html_photo', 'is_published', 'cat_id')
    # перечень строк для админ панели
    list_display_links = ('id', 'title')
    # кликабельные поля
    search_fields = ('title', 'content')
    # по каким полям можно искать
    list_editable = ('is_published',)
    # указываем строку, которую можно редактировать
    list_filter = ('is_published', 'time_create')
    # поля для фильтрации - сортировки
    prepopulated_fields = {"slug": ("title",)}
    # поле слаг прописывается автоматически

    # миниатюра при редактировании поста
    # 1) поле филдс отобразит порядок и список редактируемых полей
    fields = (
        'title', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')

    # 2) отобразим не редактируемые поля, только после этого можно добавить их в ФИЛДС
    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True  # панелька сохранить-удалить будет вверху а не внизу

    # миниатюры в админ-панеле

    def get_html_photo(self, object):
        if object.photo:  # если есть фото
            return mark_safe(f"<img src='{object.photo.url}' width=50>")
        # функция марк-сэйф не будет экранировать а выполнять тэги

    get_html_photo.short_description = "Миниатюра"  # меняем название шапки на
    # миниатюра


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Green, CreenAdmin)  # регистрируем модель
admin.site.register(Category, CategoryAdmin)

# редактируем надписи в админ-панеле
admin.site.site_title = 'Админ-панель сайта микрозелень'
admin.site.site_header = 'Админ-панель сайта микрозелень'




class ProjectUpdateAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'id': 'project_update_textarea'})}
    }