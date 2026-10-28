from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.decorators import admin_required, staff_required
from .forms import CourseForm
from .models import Course
from enrollments.models import Enrollment


# Create your views here.
# --------- TODO ----------
#
# 1. Edit success and error handling for forms (e.g. deleting, editing, ...)

@login_required
def view_courses(request):
    all_courses = Course.objects.all()
    return render(request,'courses/course_list.html', {'courses':all_courses})


@admin_required
def create_course(request):
    if (request.method == 'POST'):
        course_form = CourseForm(request.POST)
        
        if (course_form.is_valid()):
            course_form.save()
            return redirect('courses')
        else:
            return HttpResponseNotAllowed(request.method)
            #return redirect('create_course')
    
    course_form = CourseForm()
    return render(request, 'courses/course_form.html', {'course_form': course_form, 'form_title': 'Create course'})


@staff_required
def edit_course(request, course_id):
    course = Course.objects.get(id=course_id)

    if (request.method == 'POST'):
        course_data = CourseForm(request.POST, instance=course)
        
        if (course_data.is_valid()):
            course_data.save()
            return redirect('courses')
        else:
            return HttpResponseNotAllowed(request.method)
            # return redirect('edit_course')

    course_data = CourseForm(instance=course)
    return render(request, 'courses/course_form.html', {'course_form':course_data, 'form_title': 'Edit course'})


@admin_required
def delete_course(request, course_id):
    course = Course.objects.get(id=course_id)
    
    if(course is not None):
        course.delete()
        
    return redirect('courses')


