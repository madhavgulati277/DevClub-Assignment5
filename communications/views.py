from keyword import kwlist
from django.shortcuts import render,redirect
from documents.models import replydocs
from grades.models import course as courses
from .models import announcement as ann
from .models import reply as replies
from .models import thread
from .forms import annform,replyform,threadform,replymodelform
from django.contrib import messages
from django.views.generic import DeleteView,UpdateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


class AnnDelete(UserPassesTestMixin,DeleteView):
    model = ann
    def get_success_url(self):
        course_id = self.get_object().course.course_id
        return reverse('announcement' , kwargs = { 'id' : course_id})

    def test_func(self):
        ann = self.get_object()
        if self.request.user == ann.author:
            return True
        return False
    
class AnnUpdate(UserPassesTestMixin,UpdateView):
    model = ann
    fields = ['title' , 'text']
    def form_valid(self, form):
        form.save()
        id = super().get_object().course.course_id
        url1 = reverse('announcement' , kwargs = {'id' : id})
        url2 = '#' + str(super().get_object().pk)
        url = url1 + url2
        return redirect(url)
    

    def get_context_data(self, **kwargs):
         context =  super().get_context_data(**kwargs)
         context['flag'] = False
         context['object'] = super().get_object()
         context['course'] = super().get_object().course
         return context
    
    def test_func(self):
        ann = self.get_object()
        if self.request.user == ann.author:
            return True
        return False
    
class ThreadDelete(UserPassesTestMixin,DeleteView):
    model = thread
    def get_success_url(self):
        course_id = self.get_object().course.course_id
        return reverse('create_thread' , kwargs = { 'id' : course_id})

    def test_func(self):
        thread = self.get_object()
        if self.request.user == thread.author:
            return True
        return False

class ThreadUpdate(UserPassesTestMixin,UpdateView):
    model = thread
    fields = ['title' , 'text']
    def form_valid(self, form):
        form.save()
        id = super().get_object().course.course_id
        t_id = super().get_object().pk
        return redirect(reverse('thread' , kwargs = {'id' : id , 't_id':t_id}))
    

    def get_context_data(self, **kwargs):
         context =  super().get_context_data(**kwargs)
         context['flag'] = False
         context['object'] = super().get_object()
         context['course'] = super().get_object().course
         return context
    
    def test_func(self):
        thread = self.get_object()
        if self.request.user == thread.author:
            return True
        return False

class ReplyDelete(UserPassesTestMixin,DeleteView):
    model = replies
    def get_success_url(self):
        course_id = self.get_object().course.course_id
        t_id = self.get_object().thread.id
        return reverse('thread' , kwargs = { 'id' : course_id , 't_id' : t_id})

    def test_func(self):
        reply = self.get_object()
        if self.request.user == reply.user:
            return True
        return False

class ReplyUpdate(UserPassesTestMixin,UpdateView):
    model = replies
    form_class = replymodelform

    def form_valid(self, form):

        form.save()
        super().get_object().replydocs_set.all().delete()
        for file in self.request.FILES.getlist('replydocs_set'):
            f = replydocs(file_name = file.name , document = file , reply = super().get_object() )
            f.save()
        
        id = super().get_object().course.course_id
        t_id = super().get_object().thread.id
        return redirect(reverse('thread' , kwargs = {'id' : id , 't_id' : t_id}))
    

    def get_context_data(self, **kwargs):
         context =  super().get_context_data(**kwargs)
         context['flag'] = False
         context['object'] = super().get_object()
         context['course'] = super().get_object().course
         context['thread'] = super().get_object().thread
         return context
    
    def test_func(self):
        reply = self.get_object()
        if self.request.user == reply.user:
            return True
        return False














def announcement(request , id):
    course = courses.objects.get(course_id = id)
    
    if (request.user.new_user.is_instructor):
        form = annform()
        context = {
        'course' : course,
        'form' : form
        }
    
        if request.method == 'POST': 
            form = annform(request.POST)
            if form.is_valid():
                titl = form.cleaned_data.get('title')
                text = form.cleaned_data.get('text')
                author = request.user
                newann = ann(title = titl ,text = text , course = course , author = author)
                newann.save()
                messages.success(request , 'Announcement created succesfully')
                return render(request,'communications/instructor_announcement.html' , context)
            else:
                messages.error(request , 'Invalid data entered; click "Create Announcement" again')
                return render(request,'communications/instructor_announcement_with_form.html' , {
                'course':course , 
                'form' : form
                })
        else:
                return render(request,'communications/instructor_announcement.html' , context)

    if (request.user.new_user.is_student):
        return render(request,'communications/student_announcement.html' , context = {
            'course' : course
        })




def create_thread(request , id):
    course = courses.objects.get(course_id = id)
    if (request.user.new_user.is_instructor):
        url = 'communications/general_discussion_forum_instructor.html'
    if (request.user.new_user.is_student):
        url = 'communications/general_discussion_forum_student.html'
    form = threadform()
    context = {
        'course' : course,
        'form' : form,
        'flag' : True     # if flag is true, then dont display form ;otherwise display form
        }
    if request.method == 'POST': 
        form = threadform(request.POST)
        if form.is_valid():
                titl = form.cleaned_data.get('title')
                text = form.cleaned_data.get('text')
                author = request.user
                newthread = thread(title = titl ,text = text , course = course,author = author )
                newthread.save()
                messages.success(request , 'Thread created succesfully')
                return render(request,url , context)
        else:
                messages.error(request , 'Invalid data entered; click "Create Thread" again')
                return render(request,url , {
                'course':course , 
                'form' : form ,
                'flag' : False
                })
    else:
                return render(request,url , context)
        

    
    




def create_reply(request , id , t_id):
    course = courses.objects.get(course_id = id)
    thr = thread.objects.get(pk = t_id)
    form = replyform() 
    context = {
        'course' : course ,
        'thread' : thr ,
        'form' : form,
        'flag' : True   # if flag is true, then dont display form ;otherwise display form
    }

    

    if (request.user.new_user.is_instructor):
         url = 'communications/thread_instructor.html'

    if (request.user.new_user.is_student):
        url = 'communications/thread_student.html'
    
    if (request.method == 'POST') :
            form = replyform(request.POST , request.FILES) 
            if form.is_valid():
                reply_subject = form.cleaned_data.get('subject')
                reply_text = form.cleaned_data.get('text')
                user = request.user
                


                reply = replies(subject = reply_subject , text = reply_text , course = course , user = user , thread = thr )
                reply.save()
                for file in request.FILES.getlist('replydocs'):
                    f = replydocs(file_name = file.name , document = file , reply = reply )
                    f.save()
                return render(request , url , context)
            else:
                messages.error(request , 'invalid data entered') 
                context['form'] = form 
                context['flag']=False
                return render(request , url, context)
    
    else:
        return render(request , url , context)
    
    





          
        
        