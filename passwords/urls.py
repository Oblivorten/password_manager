from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('passwords/', views.password_list, name='password_list'),
    path('passwords/add/', views.password_add, name='password_add'),
    path('passwords/generate/', views.generate_random_password_view, name='generate_random_password'),
    path('login/', views.login_view, name='login'),
    path('passwords/delete/<int:password_id>/', views.password_delete, name='password_delete'),
    path('passwords/edit/<int:password_id>/', views.password_edit, name='password_edit'),
]