from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.auth_choice_view, name='auth_choice'),  # Корневой путь приложения
    path('register/', views.register_initial_view, name='register_initial'),
    path('security-questions/', views.security_questions_view, name='security_questions'),
    path('verify-code/', views.verify_code_view, name='verify_code'),
    path('home/', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
]