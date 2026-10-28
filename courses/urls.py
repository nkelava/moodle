from django.urls import path
from . import views


# Set your urls here.

urlpatterns = [
    path('', views.view_courses, name='courses'),
    path('create/', views.create_course, name='create_course'),
    path('<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('<int:course_id>/delete/', views.delete_course, name='delete_course'),
]
