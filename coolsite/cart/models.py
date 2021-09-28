from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from green.models import Green


User = get_user_model()
# settings.AUTH_USER_MODEL


class Order(models.Model):

    user = models.ForeignKey(
        User, verbose_name='Покупатель', on_delete=models.CASCADE)
    final_price = models.DecimalField(
        max_digits=9, default=0, decimal_places=2, verbose_name='К оплате')

    def __str__(self):
        return f"Order {self.id} for {self.user}"

    def get_absolute_url(self):
        return reverse('cart', kwargs={'cart_id': self.id})

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        ordering = ['user']


class OrderLineItem(models.Model):
    product = models.ForeignKey(
        Green, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Кол-во")
    price = models.DecimalField(
        max_digits=9, default=0, decimal_places=2, verbose_name='Стоимость')
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, verbose_name="Заказ")
