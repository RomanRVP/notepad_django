from django import views
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import UserAddCategoryForm
from .models import Category


class BaseView(views.View):
    """
    Заглушка (для домашней страницы).
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'notepad/base.html')


class RegistrationUser(CreateView):
    """
    Регистрация пользователя.
    """
    template_name = 'notepad/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    """
    Авторизация пользователя.
    """
    template_name = 'notepad/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('homepage')


class LogoutUser(LogoutView):
    """
    Выход из учетной записи.
    """
    next_page = 'homepage'


class UserAddCategoryView(views.View):
    """
    Добавление категории пользователем.
    """
    def get(self, request, *args, **kwargs):
        form = UserAddCategoryForm()
        context = {'form': form}
        return render(request, 'notepad/user_add_category.html', context)

    def post(self, request, *args, **kwargs):
        form = UserAddCategoryForm(request.POST)
        context = {'form': form}
        template = 'notepad/user_add_category.html'
        if form.is_valid() and request.user.is_authenticated:
            try:
                form.cleaned_data['owner'] = request.user
                obj = Category(**form.cleaned_data)
                obj.save()
                context['message'] = f'Категория ' \
                                     f'{form.cleaned_data["name"]} создана'
            except IntegrityError:
                context['message'] = 'Категория с данным именем уже существует'
                return render(request, template, context)

            # В случае успешного создания категории:
            return render(request, template, context)

        else:
            context['message'] = 'Ошибка.'
            if not form.is_valid():
                context['message'] += ' Форма заполнена неверно.'
            if not request.user.is_authenticated:
                context['message'] += ' Вам необходимо авторизоваться.'

        return render(request, template, context)
