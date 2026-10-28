from django.db import models
from .enums import OptionalChoices


# Create your models here.

class Course(models.Model):
    name                    = models.CharField(max_length=255, null=False)
    course_code             = models.CharField(max_length=16, null=False, unique=True)
    curriculum              = models.TextField(null=False)
    ects                    = models.PositiveIntegerField(null=False)
    full_time_semester      = models.PositiveIntegerField(null=False)
    part_time_semester      = models.PositiveIntegerField(null=False)
    optional                = models.CharField(max_length=8, 
                                               choices=[ (tag.name, tag.value) for tag in OptionalChoices ],
                                               default=OptionalChoices.NO,
                                               null=False)
    
    def __str__(self):
        return f'{self.name} {self.course_code}'


