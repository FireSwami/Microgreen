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
    username = forms.IntegerField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-input'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User  # стандартная модель ЮЗЕР, работает с таблицей AUTH_USER в БД
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    # username1 = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username1', 'username','password')


class ContactForm(forms.Form):  # наследуется от общего класса форм

    # далее 4 поля: имя, почта, полее ввода, капча
    #name = forms.CharField(label='Имя', max_length=255)
    subject = forms.CharField(label='Имя', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email')
    mobile = forms.IntegerField(widget=forms.TextInput, label='Телефон')
    #content = forms.CharField(label='Напишите нам', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    content = forms.CharField(label='Напишите нам', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    #captcha = CaptchaField(label='Введите текст с картинки',)
