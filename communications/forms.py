from django import forms
from documents.models import replydocs,reply_path
from .models import reply
from tinymce.widgets import TinyMCE

class annform(forms.Form):
    title = forms.CharField(max_length=30)
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))


class replyform(forms.Form):
    subject = forms.CharField(max_length=30)
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    replydocs = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}) , required=False 
        , label='attachments') 

class threadform(forms.Form):
    title = forms.CharField(max_length=30)
    text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

class replymodelform(forms.ModelForm):
    replydocs_set = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}) , required=False 
        , label='Attachments') 
    class Meta:
        model = reply
        fields=['subject' , 'text' , 'replydocs_set']
        
