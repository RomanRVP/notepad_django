from django import forms

from .models import Notepad, Category, PageForNotepad


class UserAddCategoryForm(forms.Form):
    """
    Форма для создания категории пользователем.
    """
    name = forms.CharField(max_length='255', label='Название категории',
                           error_messages={
                               'required': 'Имя категории не может быть пустым'
                           })


class UserAddNotepadForm(forms.ModelForm):
    """
    Форма для создания блокнота пользователем.
    """
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(
            owner=user_id)

    class Meta:
        model = Notepad
        fields = ('title', 'category')
        error_messages = {
            'title': {'required': 'Название блокнота не может быть пустым!'},
        }


class UserAddPageForm(forms.ModelForm):
    """
    Форма для создания страницы, в определённом блокноте.
    """
    def __init__(self, user_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notepad'].queryset = Notepad.objects.filter(owner=user_id)

    class Meta:
        model = PageForNotepad
        fields = ('notepad', 'title', 'page_text')
        error_messages = {
            'title': {'required': 'Имя страницы не может быть пустым.'},
            'page_text': {'required': 'Текст страницы не может быть пустым.'},
        }
