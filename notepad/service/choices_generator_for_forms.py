from ..models import Category, Notepad


def generate_choices_for_category(user_id):
    """
    Функция возвращает двумерный кортеж,
    в котором хранится id категории и ее имя (для конкретного пользователя).
    """
    queryset = Category.objects.filter(owner=user_id)
    return ((i.pk, i.name) for i in queryset)


def generate_choices_for_notepad(user_id):
    """
    Функция возвращает двумерный кортеж,
    в котором хранится id блокнота и его имя (для конкретного пользователя).
    """
    queryset = Notepad.objects.filter(owner=user_id)
    return ((i.pk, i.title) for i in queryset)
