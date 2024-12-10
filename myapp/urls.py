from django.urls import path
from django.shortcuts import redirect
from . import views

urlpatterns = [

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify_otp/', views.verify_otp_view, name='verify_otp'),
    path('user/', views.user_view, name='user'),
    path('admin/', views.admin_view, name='admin'),
    path('logout/', views.logout_view, name='logout'),
]