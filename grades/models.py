from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from  users.models import *



class course(models.Model):
    course_id = models.CharField(max_length=15,default='')
    course_name = models.CharField(max_length = 60)
    course_instructor = models.ForeignKey(instructor , on_delete=models.CASCADE)
    course_info = models.TextField()
    course_students = models.ManyToManyField(student , through='grades')
    in_progress = models.BooleanField(default = True)
    past = models.BooleanField(default = False)
    future = models.BooleanField(default=False)

    def __str__(self):
        return self.course_name

class grades(models.Model):
    user = models.ForeignKey(student , on_delete=models.CASCADE , null=True , blank = True)
    course = models.ForeignKey(course , on_delete=models.CASCADE , null = True , blank = True)
    
   

class grades_inline(admin.TabularInline):
    model = grades
    extra = 1

class courseAdmin(admin.ModelAdmin):
    inlines = (grades_inline,)

class studentAdmin(admin.ModelAdmin):
    inlines = (grades_inline,)



