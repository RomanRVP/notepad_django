from django import views
from django.contrib.auth.forms import UserCreationForm
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

    # ! В будущем изменить редирект на логин. !
    success_url = reverse_lazy('homepage')
