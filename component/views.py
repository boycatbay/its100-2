from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout

from .forms import announces
from .studentslist import studentlist
from .studentgetinfo import studentgetinfo as studentin
from .getMail import studentMail
from .classroomAccessAPI import *
# Create your views here.



def index(request):
    if request.user.is_authenticated:
        template = loader.get_template('component/landing.html')
    else:
        template = loader.get_template('component/index.html')
    
    return HttpResponse(template.render({}, request))

def landing(request):
    if request.user.is_authenticated:
        template = loader.get_template('component/landing.html')
    else:
        template = loader.get_template('component/index.html')
    return HttpResponse( template.render({}, request))
    

    
def announce(request):
    # if this is a POST request we need to process the form data
    if request.user.is_authenticated:
        template = 'component/announce.html'
        anouncList = getAnnouncment(request)
        first=anouncList[0].get('text'),anouncList[0].get('id'),anouncList[0].get('creationTime')
        second=anouncList[1].get('text'),anouncList[1].get('id'),anouncList[1].get('creationTime')
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = announces(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                text = form.cleaned_data['textarea']
                matrl = form.cleaned_data['material']
                makeAnnouncment(request,text)
                # redirect to a new URL:
                return render(request, 'component/landing.html')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = announces()
    else:
        template = 'component/index.html'

    return render(request, template, {'form': form,'text1':first,'text2':second})

def studentslist(request):
    if request.user.is_authenticated:
        template = 'component/studentslist.html'
        studentlists = studentlist()
    else:
        template = 'component/index.html'
    return render(request, template, {'studentlist': studentlists})


def studentgetinfo(request):
    if request.user.is_authenticated:
        template = 'component/studentinfo.html'
        uID = int(request.GET.get('userId'))
        studentInfo = studentin(uID)
        studentName = studentInfo['profile'].get('name').get('fullName')
        studentInfos = studentMail(uID)
        studentMails = studentInfos['emailAddress']
        studentPhoto = studentInfos['photoUrl']
    else:
        template = 'component/index.html'
    return render(request, template, {'studentName':studentName,'studentMail':studentMails,'studentPhoto':studentPhoto})

def logout(request):
    if request.user.is_authenticated:
        template = 'component/index.html'
        auth_logout(request)
        
    return render(request, template, {})








    

