from django.forms import ModelForm
from .models import Course


# Create your froms here.

class CourseForm(ModelForm):
    class Meta:
        model   = Course
        fields  = ['name', 'course_code', 'curriculum', 'ects', 'full_time_semester', 'part_time_semester', 'optional']
        
        
