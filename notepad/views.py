from django import views
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView


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
