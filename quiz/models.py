from django.db import models
from datetime import time
from grades.models import grades,course
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from users.models import student

def validate_positive(value):
    if value <= 0:
        raise ValidationError(
            _('question number should be positive'),
            params={'value': value},
        )


class question_bank(models.Model):
    
    course = models.OneToOneField(course , on_delete = models.CASCADE)

    def __str__(self):
        course = self.course
        return f'{course.course_name} Question Bank'


class quiz(models.Model):
    
    quiz_name = models.CharField(max_length=20)
    quiz_date_time = models.DateTimeField(null=False)
    quiz_duration = models.DurationField(null=False)
    quiz_window = models.DurationField(null=False)
    course = models.ForeignKey(course , on_delete = models.CASCADE)
    students = models.ManyToManyField(student , through = 'quiz_grade')

class quiz_grade(models.Model):
    quiz = models.ForeignKey(quiz , on_delete = models.CASCADE)
    student = models.ForeignKey(student , on_delete = models.CASCADE)
    grade = models.IntegerField(default = 0)
    attempted = models.BooleanField(default = False)

class question(models.Model):
    question = models.TextField(default = '')
    question_number = models.BigAutoField(primary_key=True)
    question_bank = models.ForeignKey(question_bank , on_delete=models.CASCADE)
    mcq_flag = models.BooleanField(default=True)
    marks = models.IntegerField(validators=[validate_positive])
    quiz = models.ForeignKey(quiz , on_delete = models.CASCADE)

class mcq_question(question):
    
    option1 = models.TextField(default = '')
    option2 = models.TextField(default = '')
    option3 = models.TextField(default = '')
    option4 = models.TextField(default = '')

    answer = models.IntegerField()


class subjective_question(question):
    
    answer = models.TextField(default ='')








