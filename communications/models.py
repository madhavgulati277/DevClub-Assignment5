from django.db import models
from grades.models import course

from django.contrib.auth.models import User

from tinymce import models as tinymce_models


class announcement(models.Model):
    title = models.CharField(max_length=50)
    text = tinymce_models.HTMLField()
    course = models.ForeignKey(course , on_delete=models.CASCADE)
    author = models.ForeignKey(User , on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title 


class thread(models.Model):
    title = models.CharField(max_length=50)
    text = tinymce_models.HTMLField()
    course = models.ForeignKey(course , on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.title 

class reply(models.Model):
    subject = models.CharField(max_length=50)
    text = tinymce_models.HTMLField()
    course = models.ForeignKey(course , on_delete=models.CASCADE)
    user = models.ForeignKey(User , on_delete= models.SET_NULL , null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    thread = models.ForeignKey(thread ,on_delete=models.CASCADE)
    

    def __str__(self):
        return self.subject


# class message(models.Model):
#     text = models.TextField()
#     sender = models.ForeignKey(User , on_delete=models.CASCADE)
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add=True)
