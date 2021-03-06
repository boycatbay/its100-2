from django.urls import path

from . import views

from django.conf import settings

from django.conf.urls.static import static

app_name = 'component'

urlpatterns = [

    path('', views.index, name='index'),
     

    path('landing/', views.landing, name='landing'),
    path('announce/', views.announce, name='announce'),
    path('student/',views.studentslist,name='studentlist'),
    path('student/info/',views.studentgetinfo,name='studentgetinfo'),
    path('student/info/assignment/detail/',views.assignmentWork,name='assignmentWork'),
    path('coursework/',views.courseWork,name='courseWork'),
    path('uploadcoursework/',views.uploadCourework,name='uploadCoursework'),
    path('settings/',views.settings,name='settings'),
    path('plagarism/',views.plagiarism,name='plagiarism'),
    path('logout/',views.logout,name='logout'),
    path('error/',views.error,name='error'),
    
   
]#+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
