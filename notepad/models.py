from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Категория блокнота.
    По большей части для того, что бы пользователь мог фильтровать блокноты.
    """
    name = models.CharField(max_length=255, verbose_name='Название категории')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name='Владелец категории')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        # Что бы категории не дублировались, добавим uniq_together:
        unique_together = ('name', 'owner')


class Notepad(models.Model):
    """
    Модель персонального блокнота, создаваемого пользователем.
    """
    title = models.CharField(max_length=255, verbose_name='Название блокнота')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name='Владелец блокнота')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 blank=True, null=True,
                                 verbose_name='Категория блокнота',
                                 related_name='Notepad')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блокнот'
        verbose_name_plural = 'Блокноты'


class PageForNotepad(models.Model):
    """
    Страница(глава) для блокнота.
    """
    notepad = models.ForeignKey(Notepad, on_delete=models.CASCADE,
                                verbose_name='Блокнот',
                                related_name='Page')
    title = models.CharField(max_length=100, verbose_name='Название страницы')
    page_text = models.TextField(verbose_name='Текст страницы')

    def __str__(self):
        return f'Блокнот: {self.notepad.title} \nСтраница: {self.title}'

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
