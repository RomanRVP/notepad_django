from django.db import models
from django.conf import settings


class Notepad(models.Model):
    """
    Модель персонального блокнота, создаваемого пользователем.
    """
    title = models.CharField(max_length=255, verbose_name='Название блокнота')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name='Владелец блокнота')

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
