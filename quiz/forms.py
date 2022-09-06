from urllib import request
from django import forms
from django.forms import ModelForm
from .models import mcq_question,subjective_question,question,validate_positive
from tinymce.widgets import TinyMCE

choices=[(1 , 'option 1') ,(2 , 'option 2'),(3 , 'option 3'),(4 , 'option 4') ]








class mcq_question_form(forms.Form):
    
    marks = forms.IntegerField(validators=[validate_positive])
    question = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    option1 = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    option2 = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    option3 = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    option4 = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    right_answer = forms.ChoiceField(choices=choices , widget = forms.RadioSelect)

    
class subjective_question_form(forms.Form):
    question = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    answer = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 10}))
    marks = forms.IntegerField(validators=[validate_positive])



class quiz_form(forms.Form):
    quiz_name = forms.CharField(max_length=20)
    quiz_date_time = forms.DateTimeField(required=True)
    quiz_duration = forms.DurationField(required=True)
    quiz_window = forms.DurationField(required  = True)


