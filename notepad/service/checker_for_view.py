from pytils.translit import slugify

from ..models import Notepad, Category


def check_notepad_with_user_slug_ang_category(
        user_id, notepad_slug, category_slug):
    """
    Функция проверяет существует ли конкретный блокнот у пользователя и
    возвращает либо блокнот (в случае успеха), либо False.
    """
    if category_slug == 'None':
        notepad = Notepad.objects.filter(owner=user_id,
                                         slug=notepad_slug).first()
        return notepad
    else:
        category = Category.objects.filter(owner=user_id,
                                           slug=slugify(category_slug)).first()
        if category:
            notepad = Notepad.objects.filter(owner=user_id,
                                             slug=notepad_slug,
                                             category=category.id).first()
            return notepad
    return False
