from django import forms


class UserAddCategoryForm(forms.Form):
    """
    Форма для создания категории пользователем.
    """
    name = forms.CharField(max_length='255', label='Название категории',
                           error_messages={
                               'required': 'Имя категории не может быть пустым'
                           })
