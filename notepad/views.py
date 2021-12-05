from django import views
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import (
    UserAddCategoryForm,
    UserAddNotepadForm,
    UserAddPageForm,
    UserDeleteCategoryForm,
    UserDeleteNotepadForm
)
from .models import Category, Notepad, PageForNotepad
from .service.context_for_forms import get_error_context_for_forms
from .service.context_for_views import (
    get_context_for_home_page_with_specific_category_view,
    get_context_for_detail_notepad_view
)


class HomePage(views.View):
    """
    Главная страница (со списком категорий и блокнотов пользователя).
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = {
                'categories_list': Category.objects.filter(owner=request.user),
                'notepads_list': Notepad.objects.filter(owner=request.user)
            }
        else:
            context = None
        return render(request, 'notepad/base.html', context=context)


class HomePageWithSpecificCategoryView(views.View):
    """
    Главная страница
    (со списком категорий и блокнотов пользователя в определённой категории).
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = get_context_for_home_page_with_specific_category_view(
                request.user, kwargs.get('slug')
            )
        else:
            context = None
        return render(request, 'notepad/base.html', context=context)


class NotepadDetailView(views.View):
    """
    Просмотр конкретного блокнота (и его страниц соответственно).
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = get_context_for_detail_notepad_view(
                request.user,
                kwargs.get('category_slug'),
                kwargs.get('notepad_slug'),
                kwargs.get('page_num')
            )
        else:
            context = None
        return render(request, 'notepad/notepad_detail.html', context=context)


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
            context['message'] = get_error_context_for_forms(
                form.is_valid(), request.user.is_authenticated)
        return render(request, template, context)


class UserAddNotepadView(views.View):
    """
    Создание блокнота пользователем.
    """
    def get(self, request, *args, **kwargs):
        form = UserAddNotepadForm(request.user.id)
        context = {'form': form}
        return render(request, 'notepad/user_add_notepad.html', context)

    def post(self, request, *args, **kwargs):
        form = UserAddNotepadForm(request.user.id, request.POST)
        context = {'form': form}
        template = 'notepad/user_add_notepad.html'
        if form.is_valid() and request.user.is_authenticated:
            form.cleaned_data['owner'] = request.user
            obj = Notepad(**form.cleaned_data)
            obj.save()
            context['message'] = f'Блокнот {form.cleaned_data["title"]} ' \
                                 f'был создан.'
            return render(request, template, context)
        else:
            context['message'] = get_error_context_for_forms(
                form.is_valid(), request.user.is_authenticated)
        return render(request, template, context)


class UserAddPageView(views.View):
    """
    Создание страницы в блокноте.
    """
    def get(self, request, *args, **kwargs):
        form = UserAddPageForm(request.user.id)
        context = {'form': form}
        return render(request, 'notepad/user_add_page.html', context)

    def post(self, request, *args, **kwargs):
        form = UserAddPageForm(request.user.id, request.POST)
        context = {'form': form}
        template = 'notepad/user_add_page.html'
        if form.is_valid() and request.user.is_authenticated:
            obj = PageForNotepad(**form.cleaned_data)
            obj.save()
            context['message'] = f'Страница {form.cleaned_data["title"]} ' \
                                 f'в блокноте {form.cleaned_data["notepad"]}' \
                                 f' была создана.'
            return render(request, template, context)
        else:
            context['message'] = get_error_context_for_forms(
                form.is_valid(), request.user.is_authenticated)
        return render(request, template, context)


class UserDeleteCategoryView(views.View):
    """
    Удаления категории пользователем.
    """
    def get(self, request, *args, **kwargs):
        form = UserDeleteCategoryForm(request.user.id)
        context = {'form': form}
        return render(request, 'notepad/user_del_category.html', context)

    def post(self, request, *args, **kwargs):
        form = UserDeleteCategoryForm(request.user.id, request.POST)
        context = {'form': form}
        template = 'notepad/user_del_category.html'
        if form.is_valid() and request.user.is_authenticated:
            category_id = form.cleaned_data['choice_category_for_delete']
            if category_id:
                obj = Category.objects.get(pk=category_id)
                category_name = obj.name
                obj.delete()
                context['message'] = f'Категория {category_name} была удалена.'
            else:
                context['message'] = 'Что бы удалить категорию, ' \
                                     'сперва нужно её выбрать.'
            return render(request, template, context)
        else:
            context['message'] = get_error_context_for_forms(
                form.is_valid(), request.user.is_authenticated)
        return render(request, template, context)


class UserDeleteNotepadView(views.View):
    """
    Удаления блокнота пользователем.
    """
    def get(self, request, *args, **kwargs):
        form = UserDeleteNotepadForm(request.user.id)
        context = {'form': form}
        return render(request, 'notepad/user_del_notepad.html', context)

    def post(self, request, *args, **kwargs):
        form = UserDeleteNotepadForm(request.user.id, request.POST)
        context = {'form': form}
        template = 'notepad/user_del_notepad.html'
        if form.is_valid() and request.user.is_authenticated:
            notepad_id = form.cleaned_data['choice_notepad_for_delete']
            if notepad_id:
                obj = Notepad.objects.get(pk=notepad_id)
                notepad_title = obj.title
                obj.delete()
                context['message'] = f'Блокнот {notepad_title} был удален.'
            else:
                context['message'] = 'Что бы удалить блокнот, ' \
                                     'сперва нужно его выбрать.'
            return render(request, template, context)
        else:
            context['message'] = get_error_context_for_forms(
                form.is_valid(), request.user.is_authenticated)
        return render(request, template, context)
