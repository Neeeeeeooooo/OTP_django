from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('verify_otp/', views.verify_otp_view, name='verify_otp'),
    path('user/', views.user_view, name='user'),
    path('teacher/', views.admin_view, name='teacher'),
    path('logout/', views.logout_view, name='logout'),
]