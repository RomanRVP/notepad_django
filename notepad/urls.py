from django.urls import path

from .views import (
    RegistrationUser,
    BaseView,
    LoginUser,
    LogoutUser,
    UserAddCategoryView,
    UserAddNotepadView,
    UserAddPageView,
    UserDeleteCategoryView
)

urlpatterns = [
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('add_category/', UserAddCategoryView.as_view(), name='add_category'),
    path('add_notepad/', UserAddNotepadView.as_view(), name='add_notepad'),
    path('add_page/', UserAddPageView.as_view(), name='add_page'),
    path('del_category/', UserDeleteCategoryView.as_view(),
         name='del_category'),
    path('', BaseView.as_view(), name='homepage')
]
