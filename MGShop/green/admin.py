from django.contrib import admin
from django import forms
from django.forms import Textarea
from django.utils.safestring import mark_safe
from .models import Green, Category, models
from ckeditor_uploader.widgets import CKEditorUploadingWidget



class GreenAdminForm(forms.ModelForm):
    content = forms.CharField(label='Статья', widget=CKEditorUploadingWidget())

    class Meta:
        model = Green
        fields = '__all__'


class CreenAdmin(admin.ModelAdmin):
    list_display = ('title', 'cat', 'price', 'available',
                    'time_create', 'get_html_photo', 'is_published')
    list_display_links = ('title',)
    search_fields = ('title', 'content', 'price')
    list_editable = ('is_published', 'available',)
    form = GreenAdminForm
    list_filter = ('available', 'is_published', 'time_create')
    prepopulated_fields = {"slug": ("title",)}
    fields = (
        'title', 'price', 'slug', 'cat', 'content', 'photo', 'get_html_photo', 'is_published', 'time_create', 'time_update')

    readonly_fields = ('time_create', 'time_update', 'get_html_photo')
    save_on_top = True

    def get_html_photo(self, object):
        if object.photo:
            return mark_safe(f"<img src='{object.photo.url}' width=50>")

    get_html_photo.short_description = "Миниатюра"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Green, CreenAdmin)
admin.site.register(Category, CategoryAdmin)


# надписи в админ-панеле
admin.site.site_title = 'Админ-панель сайта микрозелень'
admin.site.site_header = 'Админ-панель сайта микрозелень'


# ckeditor
class ProjectUpdateAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': Textarea(
            attrs={'id': 'project_update_textarea'})}
    }
