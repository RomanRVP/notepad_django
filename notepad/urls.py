from django.urls import path
from .views import RegistrationUser, BaseView


urlpatterns = [
    path('registration/', RegistrationUser.as_view(), name='registration'),
    path('', BaseView.as_view(), name='homepage')
]
