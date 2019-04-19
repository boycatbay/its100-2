from django.shortcuts import render,redirect
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

def index(request):
    if request.user.is_authenticated :
        if has_group(request.user,'TA') or has_group(request.user,'Instructor'):
            return redirect('/landing')
        else:
            template = 'component/index.html'
            return render(request, template, {})
    else:
        template = 'component/index.html'
        return render(request, template, {})

    


def landing(request):
    if request.user.is_authenticated :
        template = 'component/landing.html'
        userProfile = getuserProfile(request)
        name = userProfile['name']['fullName']
        pic = userProfile['photoUrl']
        http = 'http:'
        if http not in  pic :
            pic = http+pic
        if 'cours' in request.POST:
            ans = request.POST.get('couser')
            
            request.session['courseId'] = ans
            request.session['courseName'] = 

        elif  'courseId' in request.session:
            ans = request.session['courseId']
            
            
        elif 'courseId' not in request.session:
            ans = 'none'
            
        courseLists = getcousreList(request)    
        return render(request, template, {'name':name,'pic':pic,'courseLists':courseLists,'ans':ans})
    else:
        return redirect('/')


def announce(request):
    # if this is a POST request we need to process the form data
    if request.user.is_authenticated and 'courseId'  in request.session:
        template = 'component/announce.html'
        courseId = request.session['courseId']
        anouncList = getAnnouncment(request,courseId)
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = announces(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                text = form.cleaned_data['textarea']
                matrl = form.cleaned_data['material']
                link = matrl.split (",")
                makeAnnouncment(request,courseId,text,link)
                # redirect to a new URL:
                return redirect('/announce')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = announces()
        return render(request, template, {'form': form,'courseId':courseId ,'anouncList': anouncList})
    else:
        return redirect('/')

    


def studentslist(request):
    if request.user.is_authenticated and 'courseId'  in request.session:
        template = 'component/studentslist.html'
        courseId = request.session['courseId']
        studentlists = getStudentList(request,courseId)
        return render(request, template, {'studentlist': studentlists})
    else:
        return redirect('/')
    


def studentgetinfo(request):
    if request.user.is_authenticated and 'courseId'  in request.session:
        template = 'component/studentinfo.html'
        uID = str(request.GET.get('userId'))
        courseId = request.session['courseId']
        studentInfo = getStudentInfo(request,courseId,uID)
        studentAssignment = getpostedcoursework(request,courseId)
        submissionTime = getSubmissionTime(request,courseId,uID)
        return render(request, template, {'uId':uID,'studentinfo': studentInfo, 'studentassignment': studentAssignment,'submissionTime':submissionTime})
    else:
        return redirect('/')
   


def courseWork(request):
    if request.user.is_authenticated and 'courseId'  in request.session:
        template = 'component/coursework.html'
        courseId = request.session['courseId']
        assignmentList = getpostedcoursework(request,courseId)
        return render(request, template, {'assignmentList': assignmentList})
    else:
        return redirect('/')
    





def assignmentWork(request):
    if request.user.is_authenticated and 'courseId'  in request.session:
        template = 'component/assignmentCollection.html'
        uID = str(request.GET.get('userId'))
        courseId = request.session['courseId']
        studentInfo = getStudentInfo(request,courseId, uID)
        courseWorkId = str(request.GET.get('courseWorkId'))
        courseWorkName = str(request.GET.get('courseWorkName'))
        submissionId = str(request.GET.get('Id'))
        assignmentWork = getAssignmentwork(request,courseId,courseWorkId,submissionId)
        return render(request, template, {'studentinfo': studentInfo,'courseWorkName':courseWorkName, 'assignmentWork': assignmentWork})

    else:
        return redirect('/')
    


def uploadCourework(request):
    # if this is a POST request we need to process the form data
    if request.user.is_authenticated and 'courseId'  in request.session:
        template = 'component/uploadCoursework.html'
        courseId = request.session['courseId']
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = uploads(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                scores = form.cleaned_data['scores']
                matrl = form.cleaned_data['material']
                link = matrl.split (",")
                createAssignmentwork(request,courseId,title,description,scores,link)
                # redirect to a new URL:
                return redirect('/uploadcoursework')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = uploads()
        return render(request, template, {'form': form})
    else:
        return redirect('/')

def plagiarism(request):
    if request.user.is_authenticated and 'courseId'  in request.session:
        template = 'component/plgiarism.html'
        uID = str(request.GET.get('userId'))
        courseId = request.session['courseId']
        studentInfo = getStudentInfo(request,courseId,uID)
        studentAssignment = getpostedcoursework(request,courseId)
        return render(request, template, {'uId':uID,'studentinfo': studentInfo, 'studentassignment': studentAssignment})
    else:
        return redirect('/')
    

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        request.session.flush()
        return redirect('/')
    else:
        return redirect('/')


def error(request):
    template = 'component/error.html'
    return render(request,template,{})