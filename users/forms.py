from django import forms 
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import student,instructor,new_user

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 63 )
    password = forms.CharField(max_length = 63 , widget = forms.PasswordInput )

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username' , 'email']

class StudentForm(forms.ModelForm):
    class Meta :
        model = student
        fields=['profile_pic']
        
class InstructorForm(forms.ModelForm):
    class Meta :
        model = instructor
        fields=['profile_pic']

class UserRegister(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username' , 'email' , 'password1' , 'password2']


class New_User_Form(forms.ModelForm):
    class Meta:
        model = new_user
        fields = ['user' , 'is_student' , 'is_instructor']
        