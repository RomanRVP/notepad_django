from django.urls import path

from .views import RegistrationUser, BaseView, LoginUser, LogoutUser


urlpatterns = [
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
    path('', BaseView.as_view(), name='homepage')
]
