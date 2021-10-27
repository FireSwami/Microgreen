"""
1) Проверка выполнения входа на сайт по сравнению заголовка страницы
2) Проверка наличия кнопки "Купить на странице"
3) Проверка остальных важных страниц сайта

"""

from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.test import Client
from django.test import TestCase
from django.urls import reverse
from green.models import Category, Green


class TestPages(TestCase):

    def setUp(self):
        USERNAME = 'test'
        PASSWORD = 'Testpassword1'
        User = get_user_model()
        user = User.objects.create_user(username=USERNAME, password=PASSWORD)

        client = Client()
        client.login(username=USERNAME, password=PASSWORD)

        category = Category(name="tovar_cat", slug="microgreen_cat")
        category.save()

        green = Green(title="tovar", slug="microgreen", cat=category)
        green.save()

    def tearDown(self):
        client = Client()
        client = client.logout()

    def test_main(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        title = BeautifulSoup(response.content, 'lxml').title.text
        buy = BeautifulSoup(response.content, 'lxml').find(
            class_='buy').get("value")
        self.assertEqual(title, "Микрозелень")
        self.assertEqual(buy, "Купить")

    def test_about(self):
        about = reverse('about')
        response = self.client.get(about)
        self.assertEqual(response.status_code, 200)

        title = BeautifulSoup(response.content, 'lxml').title.text
        self.assertEqual(title, "Содержание:")

    def test_login(self):
        login = reverse('login')
        response = self.client.get(login)
        self.assertEqual(response.status_code, 200)

        title = BeautifulSoup(response.content, 'lxml').title.text
        self.assertEqual(title, "Авторизация")

    def test_contact(self):
        contact = reverse('contact')
        response = self.client.get(contact)
        self.assertEqual(response.status_code, 200)

        title = BeautifulSoup(response.content, 'lxml').title.text
        self.assertEqual(title, "Обратная связь")

    def test_admin(self):
        response = self.client.get('/admin/', follow=True)
        self.assertEqual(response.status_code, 200)

        title = BeautifulSoup(response.content, 'lxml').title.text
        self.assertEqual(title, "Войти | Админ-панель сайта микрозелень")

    def test_cart(self):
        response = self.client.get('/cart/', follow=True)
        self.assertEqual(response.status_code, 200)

        title = BeautifulSoup(response.content, 'lxml').title.text
        self.assertEqual(title, "Корзина")
