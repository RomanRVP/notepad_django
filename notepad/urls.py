from django.urls import path

from .views import (
    RegistrationUser,
    BaseView,
    LoginUser,
    LogoutUser,
    UserAddCategoryView,
)

urlpatterns = [
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('add_category/', UserAddCategoryView.as_view(), name='add_category'),
    path('', BaseView.as_view(), name='homepage')
]
