from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """
    Категория блокнота.
    По большей части для того, что бы пользователь мог фильтровать блокноты.
    """
    name = models.CharField(max_length=255, verbose_name='Название категории')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name='Владелец категории')
    slug = models.SlugField(default='', editable=False)

    def save(self, *args, **kwargs):
        # ! Kludge !
        # Делаем уникальный слаг для каждой категории пользователя.
        # Проблема была в том, что имя "CAT#3" и "cat3" генерировали
        # одинаковый слаг ("cat3"). Данный костыль нужно будет рефакторить.
        unique_slug = slugify(self.name)
        while Category.objects.filter(owner=self.owner, slug=unique_slug):
            unique_slug += '-'
        self.slug = unique_slug
        super().save(*args, kwargs)

    def get_absolute_url(self):
        return reverse('specific_category', kwargs={'slug': self.slug})

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

    slug = models.SlugField(default='', editable=False)

    def save(self, *args, **kwargs):
        # ! Kludge !
        unique_slug = slugify(self.title)
        while Notepad.objects.filter(owner=self.owner, slug=unique_slug):
            unique_slug += '-'
        self.slug = unique_slug
        super().save(*args, kwargs)

    def get_absolute_url(self):
        return reverse('specific_notepad',
                       kwargs={'notepad_slug': self.slug,
                               'page_num': 0,
                               'category_slug': self.category})

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

    def get_absolute_url(self):
        # ! Kludge !
        # В урле нужно оставить именно номер страницы в конкретном блокноте.
        # В будущем оптимизировать это с помощью чистого SQL, либо продолжать
        # гуглить.
        # (Жуть в том, что просматривая блокнот - потенциально будет лететь
        # огромное кол-во запросов в бд, и выполняться куча циклов. Если это
        # скажется на производительности - самое простое и быстрое решение
        # которое я вижу на данный момент - это заменить номер страницы
        # блокнота на её PK(id) в URL.)
        self_page_num = PageForNotepad.objects.filter(
            notepad=self.notepad.id)
        page_num = 0
        for i in self_page_num:
            if i.id == self.id:
                break
            page_num += 1
        return reverse('specific_notepad',
                       kwargs={'notepad_slug': self.notepad.slug,
                               'page_num': page_num,
                               'category_slug': self.notepad.category})

    def __str__(self):
        return f'Блокнот: {self.notepad.title} \nСтраница: {self.title}'

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
