from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Enrollment
from courses.models import Course
from users.models import User
from users.decorators import is_staff_or_admin

# Create your views here.

def check_can_manage(user, student_id):
    # Students may only see and change their own enrollments; staff and admins any student's.
    if user.id != student_id and not is_staff_or_admin(user):
        raise PermissionDenied


@login_required
def student_enrollments(request, student_id):
    check_can_manage(request.user, student_id)
    student_enrollments = Enrollment.objects.filter(student=student_id)
    enrollment_course_id_list = [ enrollment.course.id for enrollment in student_enrollments ]    
    courses = Course.objects.filter().exclude(id__in=enrollment_course_id_list)
    student = User.objects.get(id=student_id)
    semesters = {}
    student_semester_end = 7 if student.status == "FULL_TIME" else 9
    
    # This needs optimisation, for sure, for sure, for the love of god
    if student.status == "FULL_TIME":
        for i in range(1, student_semester_end):
            semesters[i] = student_enrollments.filter(course__full_time_semester=i)
    else:
         for i in range(1, student_semester_end):
            semesters[i] = student_enrollments.filter(course__part_time_semester=i)
    # ------ OPTIMiSATION END ------
            
    return render(request, 'enrollments/student_enrollments.html', {'student': student, 'enrollments':student_enrollments, 'courses':courses, 'semesters':semesters})


@login_required
def enroll(request, course_id, student_id):
    check_can_manage(request.user, student_id)
    student = User.objects.get(id=student_id)
    course = Course.objects.get(id=course_id)
    
    check_enrollment = Enrollment.objects.filter(student=student_id, course=course_id).exists()
    
    if check_enrollment is False:
        new_enrollment = Enrollment(student=student, course=course, status="enrolled")
        
        if (new_enrollment is not None):
            new_enrollment.save()
    else:
        enrollment = Enrollment.objects.get(student=student_id, course=course_id)
        
        enrollment.status = 'enrolled'
        enrollment.save()
    
    return redirect('student_enrollments', student_id=student_id)


@login_required
def remove_enrollment(request, student_id, course_id):
    check_can_manage(request.user, student_id)
    enrollment = Enrollment.objects.filter(student=student_id, course=course_id)
    
    # Passed courses can only be removed by staff, matching what the page offers.
    if enrollment.filter(status='passed').exists() and not is_staff_or_admin(request.user):
        raise PermissionDenied
    
    if (enrollment is not None):
        enrollment.delete()
        
    return redirect('student_enrollments', student_id=student_id)


@login_required
def course_passed(request, student_id, course_id):
    check_can_manage(request.user, student_id)
    enrollment = Enrollment.objects.get(student=student_id, course=course_id)
    
    if (enrollment is not None):
        enrollment.status = 'passed'
        enrollment.save()
        
    return redirect('student_enrollments', student_id=student_id)
    

