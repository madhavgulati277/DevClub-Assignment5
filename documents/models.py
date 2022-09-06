from django.db import models
from django import forms
from communications.models import reply 
from grades.models import course

def directory_path(instance , filename):
    if (instance.folder.folder_name != ''):
        url = f'docs/{instance.section.course}/{instance.section}/{instance.folder.folder_name}/{filename}'
        return url 
    else:
        url = f'docs/{instance.section.course}/{instance.section}/{filename}'
        return url


def reply_path(instance , filename):
    reply = instance.reply
    thread = reply.thread
    course = thread.course
    url = f'docs/{course.course_name}/{thread.title}/{reply.subject}/{filename}' 
    return url 
# def create_folder(instance , filename):
#     url = f'docs/{instance.section.course}/{instance.section}/{instance.folder_name}/{filename}'
#     return url 



class section(models.Model):

    section_name = models.CharField(max_length = 20)
    course = models.ForeignKey(course , on_delete=models.CASCADE)
    time_stamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.section_name


class folder(models.Model):

    section = models.ForeignKey(section , on_delete=models.CASCADE)
    folder_name = models.CharField(max_length=20)
    
    # files = models.FileField(upload_to = create_folder)
    desc = models.TextField(default='')
    time_stamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.folder_name


class docs(models.Model):
    
    file_name = models.CharField(max_length=20 , default = '')
    section = models.ForeignKey(section , on_delete=models.CASCADE)
    document = models.FileField(upload_to = directory_path)
    desc = models.TextField(default ='')
    time_stamp = models.DateField(auto_now_add=True)
    folder = models.ForeignKey(folder , on_delete=models.CASCADE)

    def __str__(self):
        return self.file_name


class replydocs(models.Model):

    file_name = models.CharField(max_length=20 , default = '')
    document = models.FileField(upload_to = reply_path)
    reply = models.ForeignKey(reply , on_delete=models.CASCADE , null=True)

    def __str__(self):
        return self.file_name