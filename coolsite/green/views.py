from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import Green, AddPostForm, ContactForm, RegisterUserForm, LoginUserForm
from .utils import DataMixin, Category
from cart.forms import CartAddProductForm


class GreenHome(DataMixin, ListView):

    model = Green
    template_name = 'green/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        c_def = self.get_user_context(title="Микрозелень")
        return {
            **context,
            **c_def,
            "buy_form": CartAddProductForm(),
        }

    def get_queryset(self):
        return Green.objects.filter(is_published=True).select_related('cat')


# @login_required
def about(request):
    contact_list = Green.objects.all()
    paginator = Paginator(contact_list, 300)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'green/about.html', {'page_obj': page_obj, 'menu': menu, 'title': 'Содержание:'})


def thanks(request):
    return render(request, 'green/thanks.html')


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Запрошенной страницы еще нет</h1>')


class AddPage(DataMixin, LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'green/addpage.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
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


class ShowPost(DataMixin, DetailView):
    model = Green
    template_name = 'green/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class GreenCategory(DataMixin, ListView):
    model = Green
    template_name = 'green/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Green.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(
            title='Категория -' + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))


class RegisterUser(DataMixin, CreateView):

    form_class = RegisterUserForm
    template_name = 'green/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):

    form_class = LoginUserForm
    template_name = 'green/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')
