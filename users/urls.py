from django.urls import path
from . import views


# Set your urls here.

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register, name='register'),
    path('users/', views.view_users, name='users'),
    path('users/profile/', views.user_profile, name='user_profile'),
]
