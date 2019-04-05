from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout

from .forms import *
from .classroomAccessAPI import *

# Create your views here.
from django import template
from django.contrib.auth.models import Group 
from django.contrib.auth.models import User

def username_present(username):
    if User.objects.filter(username=username).exists():
        return True
    
    return False
def has_group(user, group_name): 
    return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    return True if group in user.groups.all() else False

def index(request):
    if request.user.is_authenticated:
        if has_group(request.user,'TA') or has_group(request.user,'Instructor'):
            return redirect('/landing')
        else:
            template = loader.get_template('component/index.html')
            return HttpResponse(template.render({}, request))
    else:
        template = loader.get_template('component/index.html')
        return HttpResponse(template.render({}, request))

    


def landing(request):
    if request.user.is_authenticated:
        template = 'component/landing.html'
        if 'cours' in request.POST:
            ans = request.POST.get('couser')
            form = getcousreList(request)
            userProfile = getuserProfile(request)
            name = userProfile['name']['fullName']
            pic = 'https:'+userProfile['photoUrl']
        else:
            ans = 'none'
            form = getcousreList(request)
            userProfile = getuserProfile(request)
            name = userProfile['name']['fullName']
            pic = 'https:'+userProfile['photoUrl']
    else:
        template = loader.get_template('component/index.html')
    return render(request, template, {'name':name,'pic':pic,'form':form,'ans':ans})


def announce(request):
    # if this is a POST request we need to process the form data
    if request.user.is_authenticated:
        template = 'component/announce.html'
        anouncList = getAnnouncment(request)
        first = anouncList[0].get('text'), anouncList[0].get(
            'id'), anouncList[0].get('creationTime')
        second = anouncList[1].get('text'), anouncList[1].get(
            'id'), anouncList[1].get('creationTime')
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = announces(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                text = form.cleaned_data['textarea']
                matrl = form.cleaned_data['material']
                makeAnnouncment(request, text)
                # redirect to a new URL:
                return render(request, 'component/landing.html')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = announces()
    else:
        template = 'component/index.html'

    return render(request, template, {'form': form, 'text1': first, 'text2': second})


def studentslist(request):
    if request.user.is_authenticated:
        template = 'component/studentslist.html'
        studentlists = getStudentList(request)
    else:
        template = 'component/index.html'
    return render(request, template, {'studentlist': studentlists})


def studentgetinfo(request):
    if request.user.is_authenticated:
        template = 'component/studentinfo.html'
        uID = str(request.GET.get('userId'))
        studentInfo = getStudentInfo(request, uID)
        studentAssignment = getpostedcoursework(request)
        submissionTime = getSubmissionTime(request, uID)
    else:
        template = 'component/index.html'
    return render(request, template, {'uId':uID,'studentinfo': studentInfo, 'studentassignment': studentAssignment,'submissionTime':submissionTime})


def courseWork(request):
    if request.user.is_authenticated:
        template = 'component/coursework.html'
        assignmentList = getpostedcoursework(request)
    else:
        template = 'component/index.html'
    return render(request, template, {'assignmentList': assignmentList})





def assignmentWork(request):
    if request.user.is_authenticated:
        template = 'component/assignmentCollection.html'
        uID = str(request.GET.get('userId'))
        studentInfo = getStudentInfo(request, uID)
        courseWorkId = str(request.GET.get('courseWorkId'))
        courseWorkName = str(request.GET.get('courseWorkName'))
        submissionId = str(request.GET.get('Id'))
        assignmentWork = getAssignmentwork(request,courseWorkId,submissionId)
       

    else:
        template = 'component/index.html'
    return render(request, template, {'studentinfo': studentInfo,'courseWorkName':courseWorkName, 'assignmentWork': assignmentWork})

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return redirect('/')
    else:
        template = 'component/index.html'
        return render(request, template, {})


    

def error(request):
    template = 'component/error.html'
    return render(request,template,{})