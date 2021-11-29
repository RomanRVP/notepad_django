

def get_error_context_for_forms(valid_form: bool, user_auth: bool) -> str:
    """
    Функция возвращающая контекст об ошибке, в случаях когда форма не проходит.
    (Формы создания и удаления категорий, блокнотов, страниц)
    """
    error_text = 'Ошибка.'
    if not valid_form:
        error_text += ' Форма заполнена неверно.'
    if not user_auth:
        error_text += ' Вам необходимо авторизоваться.'
    return error_text
