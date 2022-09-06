
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from PIL import Image


class new_user(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    
    is_student = models.BooleanField(default=True)
    is_instructor = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    

class instructor(models.Model):
    user = models.OneToOneField(new_user,on_delete = models.CASCADE)
    profile_pic = models.ImageField(default = 'default.jpg' , upload_to = 'instructor_profile_pics')
    instructor_id = models.CharField(default = '' ,max_length=15)

    def __str__(self):
        return self.user.__str__()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)
        size = (300,300)
        if (img.height > 300 or img.width > 300):
            img.thumbnail(size)
            img.save(self.profile_pic.path)


    
class student(models.Model):
    user =  models.OneToOneField(new_user,on_delete = models.CASCADE)
    
    entry_no = models.CharField(max_length=15)
    profile_pic = models.ImageField(default = 'default.jpg' , upload_to = 'student_profile_pics')
    
    def __str__(self):
        return self.user.__str__()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.profile_pic.path)
        size = (300,300)
        if (img.height > 300 or img.width > 300):
            img.thumbnail(size)
            img.save(self.profile_pic.path)
    
    













# class newuser_inline(admin.TabularInline):
#     model = new_user
#     extra = 1

# class course_inline(admin.TabularInline):
#     model = course
#     extra = 1




















