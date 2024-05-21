from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.get_services, name='services'),
    path("login/", views.user_login, name='login'),
    path("logout/", views.user_logout, name='logout'),
    path('appointment/', views.book_appointment, name='appointment'),
    path("profile/", views.manage_profile, name="profile"),
    path("api/appointment/<int:appointment_id>/", views.get_appointment_by_id),
    path('cancel_appointment/<int:cancel_appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('delete_pet/<int:delete_pet_id>/', views.delete_pet, name='delete_pet'),
    path("api/pet/<int:pet_id>/", views.get_pet_by_id),
]