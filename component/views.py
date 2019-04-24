from django.shortcuts import render,redirect
from django.contrib.auth import logout as auth_logout
from django.db import connection,transaction

from .forms import *
from .classroomAccessAPI import *
import random

# Create your views here.
from django import template
from django.contrib.auth.models import Group 
from django.contrib.auth.models import User
from collections import namedtuple
from django.views.generic import TemplateView


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def assignmentRandom(assignment,number):
    #checkit number
    elementsInlist = len(assignment)
    #create empty list for store orderused
    storeUsed = []
    randomAsm =[]
    for i in range(0,elementsInlist*2):
        if len(storeUsed) >= number:
            break
        else:
            randomNum = random.randint(0,elementsInlist-1)
            if randomNum not in storeUsed:
                storeUsed.append(randomNum)
                randomAsm.append(assignment[randomNum])
    return randomAsm
            
    #loop iterate 

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
        cursor = connection.cursor()
        query = "SELECT email FROM component_shardcal ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        data = namedtuplefetchall(cursor)
        email = data[0].email
        template = 'component/landing.html'
        userProfile = getuserProfile(request)
        name = userProfile['name']['fullName']
        pic = userProfile['photoUrl']
        http = 'http:'
        if http not in  pic :
            pic = http+pic
        if 'cours' in request.POST:
            ans = request.POST.get('couser')
            cousreInfo = ans.split(',')
            request.session['courseId'] = cousreInfo[0]
            request.session['courseName'] = cousreInfo[1]
            cID = request.session['courseId']  
            ans = request.session['courseId']+','+request.session['courseName']

        elif  'courseId' in request.session:
            cID = request.session['courseId']  
            ans = request.session['courseId']+','+request.session['courseName']
                
        else:
            ans = 'none'
            cID = 'none'

        courseLists = getcousreList(request)    
        return render(request, template, {'name':name,'pic':pic,'courseLists':courseLists,'ans':ans,'cID':cID,'emails':email})
    else:
        return redirect('/')


def announce(request):
    # if this is a POST request we need to process the form data
    if request.user.is_authenticated and 'courseId'  in request.session and has_group(request.user,'Instructor'):
        template = 'component/announce.html'
        courseId = request.session['courseId']
        courseName = request.session['courseName']
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
        return render(request, template, {'form': form,'courseName':courseName ,'anouncList': anouncList})
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
        courseName =  request.session['courseName'] 
        cursor = connection.cursor()
        if has_group(request.user,'Instructor'):
            if 'submit' in request.POST:
                title = request.POST.get('title')
                description = request.POST.get('description')
                maxscores = request.POST.get('maxscores')
                easymaterial = request.POST.get('easymaterial')
                mediummaterial = request.POST.get('mediummaterial')
                hardmaterial = request.POST.get('hardmaterial')
                values = [title,description,maxscores,easymaterial,mediummaterial,hardmaterial]
                query = "INSERT INTO component_assignment(title,description,score,materialeasy,materialmed,materialhard) VALUES (%s,%s,%s,%s,%s,%s) " 
                cursor.execute(query,values)
                transaction.commit()
                return redirect('/')
            
        else:
            if 'submit' in request.POST:
                
                query = "SELECT easy,med,hard FROM component_assignmentration ORDER BY id DESC LIMIT 1"
                cursor.execute(query)
                data = namedtuplefetchall(cursor)
                easyRatio = data[0].easy
                medRatio = data[0].med
                hardRatio = data[0].hard
                query = "SELECT title,description,score,materialeasy,materialmed,materialhard FROM component_assignment ORDER BY id DESC LIMIT 1"
                cursor.execute(query)
                data = namedtuplefetchall(cursor)
                title = data[0].title
                desc = data[0].description
                score = data[0].score
                easy = data[0].materialeasy
                med = data[0].materialmed
                hard = data[0].materialhard

                easyList = easy.split (",")
                finalEasy = assignmentRandom(easyList,easyRatio)

                medList = med.split (",")
                finalMed = assignmentRandom(medList,medRatio)

                hardList = hard.split (",")
                finalHard = assignmentRandom(hardList,hardRatio)

                finalAssignment = finalEasy+finalMed+finalHard

                createAssignmentwork(request,courseId,title,desc,score,finalAssignment)

                Message = "Successful release assignment"
                return redirect('/')

            else:
                Message = None
            return render(request, template ,{'Message':Message,'courseName':courseName})
    
       
    else:
        return redirect('/')


def settings(request):
    if request.user.is_authenticated and 'courseId' in request.session and has_group(request.user,'Instructor'):
        cursor = connection.cursor()
        template = 'component/setting.html'
        courseId = request.session['courseId']
        if 'submitAR' in request.POST:
            easy = request.POST.get('easy')
            med = request.POST.get('med')
            hard = request.POST.get('hard')
            values = [easy,med,hard]
            query = "INSERT INTO component_assignmentration(easy,med,hard) VALUES (%s,%s,%s) " 
            cursor.execute(query,values)
            transaction.commit()
            return redirect('/')

        elif 'submitSC' in request.POST:
            email = request.POST.get('email')
            values = [email]
            query = "INSERT INTO component_shardcal(email) VALUES (%s) " 
            cursor.execute(query,values)
            transaction.commit()
            return redirect('/')

        elif 'submitNU' in request.POST:
            email = request.POST.get('email')
            role = request.POST.get('role')
            usernames = email.split('@')[0]
            value = [usernames,email,'password123','0','1','0',usernames,usernames]
            query = "INSERT INTO auth_user(username,email,password,is_superuser,is_active,is_staff,first_name,last_name,date_joined ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,datetime('now')) " 
            cursor.execute(query,value)
            transaction.commit()

            query = "SELECT id FROM auth_user WHERE email LIKE '"+email+"'"
            cursor.execute(query)
            data = namedtuplefetchall(cursor)
            uId = data[0].id

            query = "SELECT id FROM auth_group WHERE name LIKE '"+role+"'"  
            cursor.execute(query)
            data = namedtuplefetchall(cursor)
            gId = data[0].id

            value = [uId,gId]
            query = "INSERT INTO auth_user_groups(user_id,group_id) VALUES (%s,%s) "  
            cursor.execute(query,value)
            transaction.commit()

            value = ['google-oauth2',email,uId]
            query = "INSERT INTO social_auth_usersocialauth(provider,uid,user_id,extra_data) VALUES (%s,%s,%s,'{}')"  
            cursor.execute(query,value)
            transaction.commit()

            teachers(request,email,courseId)

            return redirect('/')
        else:
            return render(request, template ,{})


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


