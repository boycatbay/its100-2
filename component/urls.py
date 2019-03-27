from django.urls import path

from . import views

from django.conf import settings


app_name = 'component'

urlpatterns = [

    path('', views.index, name='index'),
     

    path('landing/', views.landing, name='landing'),
    path('announce/', views.announce, name='announce'),
    path('student/',views.studentslist,name='studentlist'),
    path('student/info/',views.studentgetinfo,name='studentgetinfo'),
    path('logout/',views.logout,name='logout'),
   
]
