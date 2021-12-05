from ..models import Category, Notepad, PageForNotepad


def get_context_for_home_page_with_specific_category_view(user, category_slug):
    """
    Функция возвращает словарь с категориями пользователя, а также
    блокноты пользователя в конкретной категории, если таки имеются.
    """
    context = dict()
    categories_list = Category.objects.filter(owner=user)
    if categories_list:
        context['categories_list'] = categories_list
    specific_category_notepad = categories_list.filter(
        slug=category_slug
    ).first()
    if specific_category_notepad:
        notepad_list = Notepad.objects.filter(
            owner=user,
            category=specific_category_notepad.id
        )
        if notepad_list:
            context['notepads_list'] = notepad_list
    return context


def get_context_for_detail_notepad_view(
        user, category_slug, notepad_slug, page_num):
    """
    Функция возвращает блокнот определенной категории (если она указана),
    а также страницы (и конкретную страницу) если они есть в блокноте.
    """
    context = dict()

    def _get_specific_notepad_and_pages(notepad):
        if notepad:
            context['notepad'] = notepad
            pages = PageForNotepad.objects.filter(
                notepad=notepad.id
            )
            if pages:
                context['pages'] = pages
                if len(pages) > page_num:
                    context['specific_page'] = pages[page_num]

    if category_slug != 'None':
        specific_category = Category.objects.filter(
            owner=user,
            slug=category_slug
        ).first()
        if specific_category:
            specific_notepad = Notepad.objects.filter(
                owner=user,
                category=specific_category.id,
                slug=notepad_slug
            ).first()
            _get_specific_notepad_and_pages(specific_notepad)

    elif category_slug == 'None':
        specific_notepad = Notepad.objects.filter(
            owner=user,
            slug=notepad_slug
        ).first()
        _get_specific_notepad_and_pages(specific_notepad)

    return context
