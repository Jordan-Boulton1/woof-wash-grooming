from django.urls import path
from .views import register, user_login
from . import views

urlpatterns = [
    path("register/", register, name="register"),
    path('', views.home, name='home'),
    path("login/", user_login, name="login"),
]