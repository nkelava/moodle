from django.urls import path
from . import views


# Set your urls here.

urlpatterns = [
    path('', views.index, name='index'),
]
