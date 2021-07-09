from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import *
from .utils import *


class GreenHome(DataMixin, ListView):
    #  paginate_by = 3   # пагинация
    model = Green  # model - выберет из таблицы Green данные и отобразит в виде списка
    template_name = 'green/index.html'  # путь к шаблону
    # по умолчанию класс Лист вью ищет шаблон по пути green/green_list.html (имя приложения\имя модели _list.html)
    context_object_name = 'posts'  # по умолчанию создается список object_list,

    # но колеция носит имя posts, для обработки в шаблоне. т.е. либо
    # там изменить название, либо  указать context_object_name

    def get_context_data(self, *, object_list=None, **kwargs):  # функция для контекста
        context = super().get_context_data(**kwargs)  # берем существующий контекст
        c_def = self.get_user_context(title="Микрозелень")  # берем из миксина - Главная страница
        return dict(list(context.items()) + list(c_def.items()))  # объеденяем супер и миксин

    def get_queryset(self):  # функция возвращает только "для публикации"
        return Green.objects.filter(is_published=True).select_related('cat')


# select_related('cat') служит для одновременной загрузки и категорий
# потому как CAT являетя foreign key - внешним ключом в моделях,
# т.е. связывает первичную модель вимен с вторичной моделью категория
# =============== таким образом получаем ЖАДНЫЙ запрос, что позволит для категорий
#  не запрашивать снова и снова категорию.

#  @login_required   # используем как декоратор для функции/ требует авторизацию для просмотра страницы
def about(request):
    # добавим пагинацию
    contact_list = Green.objects.all()  # список зелени прочтен
    paginator = Paginator(contact_list, 300)  # экземпляр класса пагинатор и кол-вло страниц

    page_number = request.GET.get('page')  # номер текуще  страницы из гет запроса
    page_obj = paginator.get_page(page_number)  # список элементов текущей страницы

    return render(request, 'green/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'Содержание:'})


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница отсутствует!</h1>')


class AddPage(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddPostForm  # класс формы
    template_name = 'green/addpage.html'  # подключили шаблон
    success_url = reverse_lazy('home')  # адресс маршрута, куда перенаправиться
    # при добавлении статьи (указано ХОУМ)

    # лейзи - формирует маршруты, только
    # когда они понадобятся, до того они могут не существовать.

    login_url = reverse_lazy('home')  # перенаправление на главную
    raise_exception = True  # генерация ошибки при неавторизованом переходе

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):  # форм вью - базовый класс, для форм
    # которые не привязаны к моделе, т.е. не работает с БД
    form_class = ContactForm
    template_name = 'green/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        subject = form.cleaned_data['subject']
        email = form.cleaned_data['email']
        mobile = form.cleaned_data['mobile']
        content = form.cleaned_data['content']
        send_mail(subject,
                  f' Мой телефон {mobile} и почта {email}. Хочу обратиться с вопросом:\n {content}',
                  'supermicrogreen@ukr.net',
                  ['jobforsoul@gmail.com'],
                  fail_silently=False)

        return redirect('thanks')


def thanks(request):
    return render(request, 'green/thanks.html')


class ShowPost(DataMixin, DetailView):
    model = Green
    template_name = 'green/post.html'  # переназначаем адресс
    slug_url_kwarg = 'post_slug'  # переназначаем переменную (по умолчанию просто slug)
    # pk_url_kwarg = 'например_id' по умолчанию 'pk'
    context_object_name = 'post'  # переопределим, т.к. в шаблоне используется post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class GreenCategory(DataMixin, ListView):
    model = Green
    template_name = 'green/index.html'
    context_object_name = 'posts'
    allow_empty = False  # если постов нет, то не получается взять нулевой объект

    # формируем ошибку 404 в таком случает.
    # для выборки
    def get_queryset(self):  # отбираются записи для вывода, также пропишем жадный запрос
        # select_related('cat')
        return Green.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    # cat__slug - для объекта cat (ссылка на ьаблицу категория) выбирает поле слаг.

    # для меню и титулки страницы
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория -' + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):
    # form_class = UserCreationForm  # джанговский класс регистрации
    form_class = RegisterUserForm  # свой класс в forms.py
    template_name = 'green/register.html'  # ссылка на шаблон
    success_url = reverse_lazy('login')  # при успешной регистрации перенаправит сюда

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):  # функция для автомат. входа после регистрации
        user = form.save()  # сохраняем в форму
        login(self.request, user)  # джанговская функция входа
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    # form_class = AuthenticationForm  # стандартная форма джанго
    form_class = LoginUserForm  # созданная форма
    template_name = 'green/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):  # функция для выхода
    logout(request)
    return redirect('login')
