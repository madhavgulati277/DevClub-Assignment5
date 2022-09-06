from django.shortcuts import render
from .models import course as courses
from django.contrib.auth.decorators import login_required

@login_required
def coursepage(request , id ):
    course = courses.objects.get(course_id = id) 
    context = {
        'course' : course
    }

    if (request.user.new_user.is_student):
        return render(request , 'grades/student_course.html' , context)
    if (request.user.new_user.is_instructor):
        return render(request , 'grades/instructor_course.html' , context)


