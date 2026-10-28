from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
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


@login_required
def create_course(request):
    if (request.method == 'POST'):
        course_form = CourseForm(request.POST)
        
        if (course_form.is_valid()):
            course_form.save()
            return redirect('courses')
    else:
        course_form = CourseForm()
    
    # On an invalid POST the bound form is rendered again with its errors.
    return render(request, 'courses/course_form.html', {'course_form': course_form, 'form_title': 'Create course'})


@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if (request.method == 'POST'):
        course_data = CourseForm(request.POST, instance=course)
        
        if (course_data.is_valid()):
            course_data.save()
            return redirect('courses')
    else:
        course_data = CourseForm(instance=course)

    # On an invalid POST the bound form is rendered again with its errors.
    return render(request, 'courses/course_form.html', {'course_form':course_data, 'form_title': 'Edit course'})


@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
        
    return redirect('courses')


