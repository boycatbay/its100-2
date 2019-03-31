import requests
import json

# Cousre


def cousreList(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses',
        params={'access_token': social.extra_data['access_token']}
    )
    listCourse = response.json().get('courses')
    return listCourse

# UserProfile


def getuserProfile(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    email = str(social.uid)
    response = requests.get(
        'https://classroom.googleapis.com/v1/userProfiles/'+email,
        params={'access_token': social.extra_data['access_token']}
    )
    userProfile = response.json()
    return userProfile

# Announcment


def getAnnouncment(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    courseId = '19606736198'
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/announcements',
        params={
            'access_token': social.extra_data['access_token'], 'pageSize': 2}
    )
    listAnnounce = response.json().get('announcements')
    return listAnnounce


def makeAnnouncment(request, textarea):
    social = request.user.social_auth.get(provider='google-oauth2')
    courseId = '19606736198'
    announcements = {
        "assigneeMode": "ALL_STUDENTS",
        "text": textarea,
        "state": "PUBLISHED"

    }
    response = requests.post(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/announcements',
        params={'access_token': social.extra_data['access_token']}, data=json.dumps(announcements)
    )
    responsed = response.json()
    return responsed


# coursework
def postedcoursework(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    courseId = '19606736198'
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/courseWork',
        params={'access_token': social.extra_data['access_token'],
                'courseWorkStates': 'PUBLISHED', 'orderBy': 'updateTime desc'}
    )
    postedcoursework = response.json().get('courseWork')
    return postedcoursework


def getStudentList(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    courseId = '19606736198'
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/students',
        params={'access_token': social.extra_data['access_token']}
    )
    studentList = response.json().get('students')
    return studentList


def getStudentInfo(request, userId):
    social = request.user.social_auth.get(provider='google-oauth2')
    courseId = '19606736198'
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/students/'+userId,
        params={'access_token': social.extra_data['access_token']}
    )
    studentInfo = response.json()
    return studentInfo

def getStudentAssignments(request,courseWorkId,userId):
    social = request.user.social_auth.get(provider='google-oauth2')
    courseId = '19606736198'
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/courseWork/'+courseWorkId+'/studentSubmissions',
        params={'access_token': social.extra_data['access_token'],'userId':userId}
    )
    assignments = response.json().get('studentSubmissions')
    return assignments

def getPostedAssignments(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    courseId = '19606736198'
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/courseWork',
        params={'access_token': social.extra_data['access_token'],'orderBy':'updateTime desc'}
    )
    assignments = response.json().get('courseWork')
    return assignments