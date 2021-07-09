from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *


class AddPostForm(forms.ModelForm):
    #  конструктор для атозаполнения формы КАТ.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # сначала должен отработать материнский класс
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Green  # связка с классом Green
        # указываем поля к отображению '__all__' - если все не автоматические поля
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        # виджеты для кастомирования полей
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):  # валидация для поля title
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title


# создание формы. наследуем от стандартной, расширяем МЕТА
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User  # стандартная модель ЮЗЕР, работает с теблицей AUTH_USER в БД
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):  # наследуется от общего класса форм

    # далее 4 поля: имя, почта, полее ввода, капча
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    mobile = forms.ImageField(widget=forms.TextInput, label='Телефон')
    content = forms.CharField(label='Напишите нам', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField(label='Введите текст с картинки')
