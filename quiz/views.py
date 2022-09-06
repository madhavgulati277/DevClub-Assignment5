from django.shortcuts import render,redirect
from .forms import *
from grades.models import course as courses
from .models import question,mcq_question,subjective_question,quiz,quiz_grade
from django.contrib import messages
import datetime 


def create_question(request ,id,name):

    if (request.user.new_user.is_student):
        return redirect('coursepage',kwargs = {'id' : id})
    
    mcq_form = mcq_question_form()
    sub_form = subjective_question_form()
    course = courses.objects.get(course_id = id)
    qb = course.question_bank
    q = quiz.objects.get(quiz_name = name)
    marks = 0
    for question in q.question_set.all() :
        m = question.marks
        marks += m

    context = {
        'mcq_form' : mcq_form , 
        'sub_form' : sub_form , 
        'course' : course,
        'quiz' : q,
        'marks' : marks
    }


    if (request.method == 'POST'):
       
        if request.POST['type'] == 'mcq':
            form = mcq_question_form(request.POST)
            if form.is_valid():

                answer = form.cleaned_data.get('right_answer')
                question = form.cleaned_data.get('question')
                marks = form.cleaned_data.get('marks')
                option1 = form.cleaned_data.get('option1')
                option2 = form.cleaned_data.get('option2')
                option3 = form.cleaned_data.get('option3')
                option4 = form.cleaned_data.get('option4')
                mcq = mcq_question(question = question , answer = answer , option1 = option1,option2 = option2,
                                    option3 = option3, option4 = option4 , question_bank = qb,quiz = q , marks = marks)
                mcq.save()
                messages.success(request , 'Mcq question created successfully')
                return redirect('display_quiz' ,id = id , name = name)

        if request.POST['type'] == 'sub':
            form = subjective_question_form(request.POST)
            if form.is_valid():

                answer = form.cleaned_data.get('answer')
                question = form.cleaned_data.get('question')
                sub = subjective_question(question = question , answer = answer,question_bank = qb,
                                            quiz = q , marks = marks)
                sub.save()
                messages.success(request , 'Subjective question created successfully')
                return redirect('display_quiz' ,id = id , name = name)
        
    else:
        return render(request , 'quiz/create_question.html' , context)



def create_quiz(request,id):

    course = courses.objects.get(course_id = id)
    if (request.user.new_user.is_student):
        return redirect('coursepage',id=id)

    form =  quiz_form()
    
    context = {
        'form' : form ,
        'course' : course
    }

    if (request.method == 'POST'):
        form = quiz_form(request.POST)
        if form.is_valid():
            quiz_name = form.cleaned_data.get('quiz_name')
            quiz_duration = form.cleaned_data.get('quiz_duration')
            quiz_window = form.cleaned_data.get('quiz_window')
            quiz_date_time = form.cleaned_data.get('quiz_date_time')
            q = quiz(course = course , quiz_name = quiz_name , quiz_duration = quiz_duration 
            , quiz_date_time = quiz_date_time , quiz_window = quiz_window)
            q.save() 
            messages.success(request , 'Quiz created successfully')
            return redirect('coursepage',id=id)
    else:
        return render(request , 'quiz/create_quiz.html' , context)

def view_quizes(request , id):
    if (request.user.new_user.is_student):
        course = courses.objects.get(course_id = id)
        quiz_set = quiz.objects.all().filter(course = course).order_by('-quiz_date_time')
        now = datetime.datetime.now()
        list=[]
        for q in quiz_set :
            duration = q.quiz_window
            if ((now - q.quiz_date_time).total_seconds() > duration.hours*3600 + duration.minutes*60 + duration.seconds):
                list.append((q.quiz_name , 'overdue'))
            if (now>q.quiz_date_time and (now - q.quiz_date_time).total_seconds() <= duration.hours*3600 + duration.minutes*60 + duration.seconds):
                list.append((q.quiz_name , 'open'))
            else:
                pass
        context = {
            'course' : course,
            'list' : list
        }
        return render(request , 'quiz/view_quizes_student.html' , context)

    if (request.user.new_user.is_instructor):
        course = courses.objects.get(course_id = id)
        return render(request , 'quiz/view_quizes_instructor.html' , {'course' : course})

def display_quiz(request,id,name):
    course = courses.objects.get(course_id = id)
    q = quiz.objects.get(quiz_name = name)
    marks = 0
    for question in q.question_set.all() :
        m = question.marks
        marks += m
    duration = q.quiz_window
    context = {
        'course' : course , 
        'quiz' : q,
        'marks' : marks,
        'duration' : duration
    }
    if (request.user.new_user.is_student):
        if (request.user.new_user.student.quiz_grade.attempted):
            return redirect('coursepage' , id=id)

        now = datetime.datetime.now()
        
        if ((now - q.quiz_date_time).total_seconds() > duration.hours*3600 + duration.minutes*60 + duration.seconds):
            return redirect('coursepage' , id=id)
        
        if (now < q.quiz_date_time):
            return redirect('coursepage' , id=id)

        if (request.method == 'POST'):
            grade = 0
            for question in q.question_set.all() :
                if (question.mcq_flag):
                    if (request.POST[f'{question.id}'] == ''):
                        grade += 0
                    elif (int(request.POST[f'{question.id}']) == question.mcq_question.answer):
                        grade += question.marks
                    elif (int(request.POST[f'{question.id}']) != question.mcq_question.answer):
                        grade += 0
                else:
                    if (request.POST[f'{question.id}'] == ''):
                        grade += 0
                    elif (request.POST[f'{question.id}'] == question.subjective_question.answer):
                        grade += question.marks
                    elif (request.POST[f'{question.id}'] != question.subjective_question.answer):
                        grade += 0
            qg = quiz_grade(student = request.user.new_user.student , quiz = q , grade = grade, attempted = True)
            qg.save()
            return render(request , 'quiz/quiz_completed.html' , {'course' : course})
        else:
            return render(request , 'quiz/display_quiz_student.html' , context)

    else :
        return render(request , 'quiz/display_quiz_instructor.html' , context)

def display_question_bank(request , id):
    if (request.user.new_user.is_student):
        return redirect('coursepage',id=id)
    
    course = courses.objects.get(course_id = id)
    qb = course.question_bank
    context = {
        'course' : course , 
        'question_bank' : qb
    }
    return render(request , 'quiz/display_question_bank.html' , context)

def show_grades(request , id):
    course = courses.objects.get(course_id = id)
    
    if (request.user.new_user.is_student):
        quiz_set = quiz.objects.all().filter(course = course).order_by('-quiz_date_time')
        now = datetime.datetime.now()
        list=[]
        for q in quiz_set :
            duration = q.quiz_window
            if ((now - q.quiz_date_time).total_seconds() > duration.hours*3600 + duration.minutes*60 + duration.seconds):
                marks = request.user.new_user.student.quiz_grade_set.all().filter(quiz = q)
                total_marks = 0
                for question in q.question_set.all() :
                    m = question.marks
                    total_marks += m
                list.append((q,marks,total_marks))
        context = {
            'course' : course ,
            'list' : list
        }
        return render(request , 'quiz/show_grades_student.html' , context)

    if (request.user.new_user.is_instructor):
        quiz_set = quiz.objects.all().filter(course = course).order_by('-quiz_date_time')
        now = datetime.datetime.now()
        list=[]
        for q in quiz_set :
            duration = q.quiz_window
            if ((now - q.quiz_date_time).total_seconds() > duration.hours*3600 + duration.minutes*60 + duration.seconds):
                marks = request.user.new_user.student.quiz_grade_set.all().filter(quiz = q)
                
                list.append(q)
        context = {
            'course' : course ,
            'list' : list
        }
        return render(request , 'quiz/show_grades_instructor.html' , context)

def show_all_grades(request,id,name):
    if (request.user.new_user.is_student):
        return redirect('coursepage',id=id)

    course = courses.objects.get(course_id = id)
    q = quiz.objects.get(quiz_name = name)
    total_marks = 0
    for question in q.question_set.all() :
        m = question.marks
        total_marks += m
    list = []
    for student in course.course_students_set.all():
        marks = student.quiz_grade_set.all().get(quiz = q).grade
        list.append((student,marks))
    context = {
        'course' : course , 
        'quiz' : q,
        'total_marks' : total_marks,
        'list' : list
    }
    return render(request , 'quiz/show_quiz_grades.html' , context)



        

