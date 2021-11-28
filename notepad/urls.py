from django.urls import path

from .views import (
    RegistrationUser,
    BaseView,
    LoginUser,
    LogoutUser,
    UserAddCategoryView,
    UserAddNotepadView,
)

urlpatterns = [
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('add_category/', UserAddCategoryView.as_view(), name='add_category'),
    path('add_notepad/', UserAddNotepadView.as_view(), name='add_notepad'),
    path('', BaseView.as_view(), name='homepage')
]
