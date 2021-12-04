from django.urls import path

from .views import (
    RegistrationUser,
    HomePage,
    LoginUser,
    LogoutUser,
    UserAddCategoryView,
    UserAddNotepadView,
    UserAddPageView,
    UserDeleteCategoryView,
    UserDeleteNotepadView,
    HomePageWithSpecificCategoryView
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
    path('del_notepad/', UserDeleteNotepadView.as_view(), name='del_notepad'),
    path('category/<str:slug>/', HomePageWithSpecificCategoryView.as_view(),
         name='specific_category'),
    path('', HomePage.as_view(), name='homepage')
]
