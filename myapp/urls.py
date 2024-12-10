# myapp/urls.py
from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('', lambda request: redirect('login')),
    path('myapp/login/', views.login_view, name='login'), 
    path('myapp/register/', views.register_view, name='register'),
    path('myapp/verify_otp/', views.verify_otp_view, name='verify_otp'),
    path('myapp/user/', views.user_view, name='user'),
    path('myapp/admin/', views.admin_view, name='admin'),
    path('myapp/logout/', views.logout_view, name='logout'),
]
