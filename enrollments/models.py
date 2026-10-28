from django.conf import settings
from django.db import models
from courses.models import Course


# Create your models here.

class Enrollment(models.Model):
    student     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    course      = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    status      = models.CharField(max_length=64, null=False)
    
    def __str__(self):
        return f'{self.student} {self.course} {self.status}'
    
    
    