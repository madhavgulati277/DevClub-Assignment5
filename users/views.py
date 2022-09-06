from django.shortcuts import render,redirect
from .forms import LoginForm,UserUpdateForm,StudentForm,InstructorForm,UserRegister,New_User_Form
from django.contrib.auth import authenticate,login,logout
from lms.settings import LOGIN_REDIRECT_URL,LOGIN_URL
from django.contrib import messages
from  django.contrib.auth.decorators import login_required



@login_required
def dashboard(request):
    if (request.user.new_user.is_student):
        return render(request , 'users/student_dashboard.html')
    if (request.user.new_user.is_instructor):
        return render(request , 'users/instructor_dashboard.html')


def login_view(request):
    form = LoginForm()
    
    if (request.user.is_authenticated):
        return redirect('dashboard') 
    
    if (request.method == 'POST'):
        form = LoginForm(request.POST)
        if (form.is_valid()):
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request , username = username , password = password)
            if (user != None):
                login(request ,user)
                return redirect('dashboard') 
            else:
                messages.error(request , 'Invalid data entered')
                return render(request,'users/login.html' , {'form' : form })
        else:
            messages.error(request,'Invalid data entered') 
            return render(request,'users/login.html' , {'form' : form})
        
        
    
    else:
       return render(request , 'users/login.html' , { 'form' : form})


def logout_view(request):
    logout(request) 
    return redirect('login')

@login_required
def profile(request):
   if (request.user.new_user.is_student):
        return render(request , 'users/student_profile.html')
   if (request.user.new_user.is_instructor):
        return render(request , 'users/instructor_profile.html')

@login_required
def update_profile(request):

    if (request.user.new_user.is_student):
        u_form = UserUpdateForm(instance=request.user)
        s_form = StudentForm(instance = request.user.new_user.student)
        context = {
            'u_form' : u_form,
            's_form' : s_form 
        }
        if (request.method == 'POST'):
            request.user.new_user.student.profile_pic.delete(save=False)
            u_form = UserUpdateForm(request.POST , instance = request.user)
            s_form = StudentForm(request.POST , request.FILES , instance = request.user.new_user.student)
            if u_form.is_valid() and s_form.is_valid():
                
                u = u_form.save()
                u.new_user.save()
                s_form.save()
                messages.success(request , f'Profile for {request.user.username} is updated successfully.')
                return redirect('profile')
            else:
                messages.error(request , f'Invalid data entered. Please try again')
                return render(request , 'users/update_student_profile.html' , context = {
            'u_form' : u_form,
            's_form' : s_form 
        })
        else:
            return render(request , 'users/update_student_profile.html' , context)


    
    if (request.user.new_user.is_instructor):
        u_form = UserUpdateForm(instance=request.user)
        i_form = StudentForm(instance = request.user.new_user.instructor)
        context = {
            'u_form' : u_form,
            'i_form' : i_form 
        }
        if (request.method == 'POST'):
            request.user.new_user.instructor.profile_pic.delete(save=False)
            u_form = UserUpdateForm(request.POST , instance = request.user)
            i_form = InstructorForm(request.POST , request.FILES , instance = request.user.new_user.instructor)
            if u_form.is_valid() and i_form.is_valid():
                
                u_form.save()
                i_form.save()
                messages.success(request , f'Profile for {request.user.username} is updated successfully.')
                return redirect('profile')
            else:
                messages.error(request , f'Invalid data entered. Please try again')
                return render(request , 'users/update_instructor_profile.html' , context = {
            'u_form' : u_form,
            'i_form' : i_form 
        })
        else:
            return render(request , 'users/update_instructor_profile.html' , context)



def register(request):
    form = UserRegister()
    
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            user = form.save()
            if request.POST['role'] == 'student':
                dict = {
                    'user' : user ,
                    'is_student' : True,
                    'is_instructor' : False
                }
            if request.POST['role'] == 'instructor':
                dict = {
                    'user' : user ,
                    'is_student' : False,
                    'is_instructor' : True
                }
            new_form = New_User_Form(dict)
            new_form.save()
            messages.success(request , 'Registration done successfully. Please update your profile by logging in')
            return redirect('login')
        else:
            messages.error(request , 'Registration done successfully. Please update your profile by logging in')
            return render(request , 'users/register.html' , context = { 'form' : form})
    else:
        return render(request , 'users/register.html' , context = { 'form' : form})