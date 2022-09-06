from email import message
from fileinput import filename
from pydoc import doc
from django.shortcuts import render,redirect
from .forms import docform,folderform,sectionform
from django.contrib import messages
from grades.models import course as courses
from .models import docs,folder,section
import datetime
from django.views.generic import DeleteView
from django.urls import reverse







def uploadfile(request , id , section_id):
    form = docform()
    course = courses.objects.get(course_id = id) 
    sec = section.objects.get(section_name = section_id)
    context = {
                'form' : form,
                'course' : course,
                'section' : sec
            }
    if (request.method == 'POST'):
        form = docform(request.POST,request.FILES)
        if (form.is_valid()):
            file = request.FILES.get('document')
            f = folder.objects.filter(section = sec).get(folder_name='')
            
            new_form = docs( folder = f ,document = file , section = sec , desc =request.POST.get('description') , file_name = request.POST.get('name'))
            new_form.save() 
            messages.success(request ,'files uploaded successfully')
            return redirect('coursepage' , id)
        else:
            messages.error(request , 'invalid data entered')
            return render(request , 'documents/uploadfile.html' , {
                'form' : form ,
                'course' : course,
                'section' : sec
            })
    else:
        return render(request , 'documents/uploadfile.html' , context)
    



def uploadfolder(request , id , section_id):
    form = folderform()
    course = courses.objects.get(course_id = id)
    sec = section.objects.get(section_name = section_id)
    context = {
        'form' : form ,
        'course' : course,
        'section' : sec
    }

    if request.method == 'POST':
        form = folderform(request.POST , request.FILES)
        
        if (form.is_valid()):
            fol = folder(desc = request.POST.get('description'),folder_name = request.POST.get('folder_name'),section = sec)
            fol.save()
            for file in request.FILES.getlist('files'):
                new_form = docs(section = sec ,folder=fol,document = file ,file_name=file.name)
                new_form.save() 
            
            messages.success(request , 'folder uploaded succesfully')
            return redirect('coursepage' ,id)
        else:
            messages.error(request , 'invalid data entered')
            return render(request , 'documents/uploadfolder.html' ,{'form' : form , 'course' : course , 'section' : sec})

    
    else:
        return render(request , 'documents/uploadfolder.html' , context)


def showfolder(request , id,section_id , folder_name):
    course = courses.objects.get(course_id = id)
    sec = section.objects.get(section_name = section_id)
    fol = folder.objects.get(folder_name = folder_name)
    context = {
        'course':course,
        'section':sec,
        'folder':fol
    }
    return render(request , 'documents/showfolder.html' , context)



def create_section(request , id):
    form = sectionform()
    course = courses.objects.get(course_id = id)
    context  = {
        'form' : form ,
        'course' : course
    }
    if request.method == 'POST':
        form = sectionform(request.POST)
        if form.is_valid():
            section_name = form.cleaned_data.get('section_name')
            sec = section(section_name = section_name , course = course )
            sec.save()
            fol = folder(folder_name = '' , section = sec , desc = '')
            fol.save()
            messages.success(request , 'section created succesfully')
            return redirect('coursepage' , id)
        else:
            messages.error(request , 'section created succesfully')
            return render(request , 'grades/instructor_course.html' , context)
    else:
        return render(request , 'documents/create_section.html' , context)




class SectionDelete(DeleteView):
    model = section
    def get_success_url(self) :
        return reverse('coursepage' , kwargs= { 'id' : self.get_object().course.course_id})
    
    

    
class FolderDelete(DeleteView):
    model = folder
    def get_success_url(self) :
        return reverse('coursepage' , kwargs= { 'id' : self.get_object().section.course.course_id})
    def get_context_data(self, **kwargs) :
         
        context = super().get_context_data(**kwargs)
        folder = self.get_object()
        section = folder.section
        course = section.course
        context['course'] = course
        return context 

class FileDelete(DeleteView):
    model = docs
    def get_success_url(self) :
        return reverse('coursepage' , kwargs= { 'id' : self.get_object().section.course.course_id})
    def get_context_data(self, **kwargs) :
         
        context = super().get_context_data(**kwargs)
        file = self.get_object()
        section = file.section
        course = section.course
        context['course'] = course
        return context 
