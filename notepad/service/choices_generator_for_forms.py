from ..models import Category


def generate_choices_for_category(user_id):
    """
    Функция возвращает двумерный кортеж,
    в котором хранится id категории и ее имя (для конкретного пользователя).
    """
    queryset = Category.objects.filter(owner=user_id)
    return ((i.pk, i.name) for i in queryset)
