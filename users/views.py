from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user, login, logout
from django.contrib.auth.decorators import login_required
from users.enums import StatusChoices, RoleChoices
from enrollments.models import Enrollment
from .decorators import staff_required
from .forms import CreateUserForm
from .models import User


# Create your views here.

@staff_required
def view_users(request):
    students    = User.objects.filter(role="STUDENT")
    professors  = User.objects.filter(role="PROFESSOR")
        
    return render(request, 'users/user_list.html', {'students':students, 'professors':professors})

@login_required
def user_profile(request):
    user            = get_user(request)
    user_courses    = Enrollment.objects.filter(student_id=user.id)
    user.status     = StatusChoices[user.status].value
    user.role       = RoleChoices[user.role].value
    
    return render(request, 'users/user_profile.html', {'user':user, 'user_courses':user_courses})


def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'GET':
            return render(request, 'users/login.html', {})
        else:
            email = request.POST.get('email')
            password = request.POST.get('password')
            
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                return redirect('login')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'GET':
        user_form = CreateUserForm()
        return render(request, 'users/register.html', {'form':user_form, 'student_role':RoleChoices.STUDENT})
    else:
        user_form = CreateUserForm(request.POST.copy())
        user_role = user_form['role'].value()
        
        # Only admins may pick a role; everyone else always registers as a student.
        if not user_role or not getattr(request.user, 'is_admin', False):
            user_form.data['role'] = RoleChoices.STUDENT.name

        if user_form.is_valid():
            user_form.save()
            return redirect('login')
        else:
            return render(request, 'users/register.html', {'form':user_form})


