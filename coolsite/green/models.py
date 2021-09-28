from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class Green(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    photo = models.ImageField(
        upload_to="photos/%Y/%m/%d/", verbose_name="Фото")
    time_create = models.DateTimeField(
        auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(
        auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    cat = models.ForeignKey(
        'Category', on_delete=models.PROTECT, verbose_name="Категории")
    price = models.DecimalField(
        default=1, max_digits=9, decimal_places=2, verbose_name='Цена')
    available = models.BooleanField(default=True, verbose_name="Наличие")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Микрозелень'
        verbose_name_plural = 'Микрозелень'
        ordering = ['time_create', 'title']


class Category(models.Model):
    name = models.CharField(
        max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True,
                            db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категория'
        ordering = ['id']
