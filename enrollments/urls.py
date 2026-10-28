from django.urls import path
from . import views


urlpatterns = [
    path('<int:student_id>/', views.student_enrollments, name='student_enrollments'),
    path('<int:student_id>/<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('<int:student_id>/<int:course_id>/pass/', views.course_passed, name='course_passed'),
    path('<int:student_id>/<int:course_id>/remove/', views.remove_enrollment, name='remove_enrollment'),
]
