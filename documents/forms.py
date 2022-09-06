from django import forms


class docform(forms.Form):
   name = forms.CharField(max_length=20)
   document = forms.FileField()
   description = forms.CharField(widget=forms.Textarea)


class folderform(forms.Form):
    folder_name = forms.CharField(max_length=20)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    description = forms.CharField(widget=forms.Textarea)

class sectionform(forms.Form):
    section_name = forms.CharField(max_length = 20)
