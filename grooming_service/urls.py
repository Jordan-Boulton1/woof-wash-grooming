from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.get_services, name='services'),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name='logout'),
]