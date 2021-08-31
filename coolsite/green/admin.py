from django.contrib import admin
from django import forms
from django.forms import Textarea
from django.utils.safestring import mark_safe
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class GreenAdminForm(forms.ModelForm):
    content = forms.CharField(label='Статья', widget=CKEditorUploadingWidget())
    class Meta:
        model = Green
        fields = '__all__'


class CreenAdmin(admin.ModelAdmin):
    list_display = ('title', 'cat', 'price', 'available', 'time_create', 'get_html_photo', 'is_published')
    # перечень строк для админ панели
    list_display_links = ('title',)
    # кликабельные поля
    search_fields = ('title', 'content', 'price')
    # по каким полям можно искать
    list_editable = ('is_published', 'available',)
    # указываем строку, которую можно редактировать
    form = GreenAdminForm
    list_filter = ('available', 'is_published', 'time_create')
    # поля для фильтрации - сортировки
    prepopulated_fields = {"slug": ("title",)}
    # поле слаг прописывается автоматически

    # миниатюра при редактировании поста
    # 1) поле филдс отобразит порядок и список редактируемых полей
    fields = (
        'title', 'price', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')

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


#Добавил ckeditor
class ProjectUpdateAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'id': 'project_update_textarea'})}
    }
