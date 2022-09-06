"""lms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from users import views as users_views
from grades import views as grades_views
from django.contrib.auth import views as login_views
from documents import views as doc_views
from communications import views as comm_views
from quiz import views as quiz_views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',users_views.login_view,name = 'login'),
    path('logout/',users_views.logout_view , name = 'logout'),
    path('dashboard/', users_views.dashboard , name = 'dashboard'),
    path('profile/' , users_views.profile , name='profile'),
    path('profile/update_profile' , users_views.update_profile , name='update_profile'),
    path('register/' , users_views.register , name='register'),
    
    path('course/<str:id>/' , grades_views.coursepage , name='coursepage'),
    
    path('tinymce/', include('tinymce.urls')),
    
    path('course/delete_ann/<str:id>/<int:pk>' , comm_views.AnnDelete.as_view() , name='delete_ann'),
    path('course/update_ann/<str:id>/<int:pk>' , comm_views.AnnUpdate.as_view() , name='update_ann'),
    path('course/delete_thread/<str:id>/<int:pk>' , comm_views.ThreadDelete.as_view() , name='delete_thread'),
    path('course/update_thread/<str:id>/<int:pk>' , comm_views.ThreadUpdate.as_view() , name='update_thread'),
    path('course/thread/<str:id>/<int:t_id>/delete_reply/<int:pk>' , comm_views.ReplyDelete.as_view() , name='delete_reply'),
    path('course/thread/<str:id>/<int:t_id>/update_reply/<int:pk>' , comm_views.ReplyUpdate.as_view() , name='update_reply'),
    path('course/announcements/<str:id>/' ,comm_views.announcement , name='announcement' ),
    path('course/create_thread/<str:id>/' ,comm_views.create_thread , name='create_thread' ),
    path('course/thread/<str:id>/<int:t_id>/' ,comm_views.create_reply , name='thread' ),

    path('course/create_section/<str:id>/' ,doc_views.create_section , name='create_section' ),
    path('course/delete_section/<str:id>/<int:pk>/' ,doc_views.SectionDelete.as_view() , name='delete_section' ),
    path('course/delete_file/<str:id>/<int:pk>/' , doc_views.FileDelete.as_view() , name="delete_file"),
    path('course/delete_folder/<str:id>/<int:pk>/' , doc_views.FolderDelete.as_view() , name="delete_folder"),
    path('course/uploadfile/<str:id>/<str:section_id>/' ,doc_views.uploadfile , name='uploadfile' ),
    path('course/uploadfolder/<str:id>/<str:section_id>/' ,doc_views.uploadfolder , name='uploadfolder' ),
    path('course/showfolder/<str:id>/<str:section_id>/<str:folder_name>/' , doc_views.showfolder , name='showfolder'),

    path('password-reset' , login_views.PasswordResetView.as_view(template_name = 'users/password_reset.html') , name=
    'password_reset'),
    path('password-reset-done' , login_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html') , name=
    'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/' , login_views.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html') , name=
    'password_reset_confirm'),
    path('password-reset-complete/' , login_views.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html') , name=
    'password_reset_complete'),

    path('course/create_question/<str:id>/<str:name>/' ,quiz_views.create_question , name='create_question' ),
    path('course/create_quiz/<str:id>/' , quiz_views.create_quiz , name='create_quiz'),
    path('course/view_quizes/<str:id>/' , quiz_views.view_quizes , name='view_quizes'),
    path('course/display_quiz/<str:id>/<str:name>/' , quiz_views.display_quiz , name='display_quiz'),
    path('course/display_question_bank/<str:id>/' , quiz_views.display_question_bank , name='question_bank'),
    path('course/show_grades/<str:id>/' , quiz_views.show_grades , name='show_grades'),
    path('course/show_all_grades/<str:id>/<str:name>' , quiz_views.show_all_grades , name='show_all_grades'),


]
if settings.DEBUG:
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



