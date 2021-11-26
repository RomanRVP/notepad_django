from django.contrib import admin
from .models import Category, Notepad, PageForNotepad


admin.site.register(Category)
admin.site.register(Notepad)
admin.site.register(PageForNotepad)
