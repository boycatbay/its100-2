import requests
import json
#import io
#from apiclient.http import MediaIoBaseDownload
# Cousre


def getcousreList(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses',
        params={'access_token': social.extra_data['access_token'],'teacherId':'me'}
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


def getAnnouncment(request,courseId):
    social = request.user.social_auth.get(provider='google-oauth2')
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/announcements',
        params={
            'access_token': social.extra_data['access_token'], 'pageSize': 3,'orderBy':'updateTime desc'}
    )
    listAnnounce = response.json().get('announcements')
    return listAnnounce


def makeAnnouncment(request,courseId,textarea,links):
    social = request.user.social_auth.get(provider='google-oauth2')
    
    announcements = {
        "assigneeMode": "ALL_STUDENTS",
        "text": textarea,
        "state": "PUBLISHED",
        "materials" : []
        
    }
    if links :
        for link in links:
            lin = {"link":{"url":link}}
            announcements["materials"].append(dict(lin))

    
    response = requests.post(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/announcements',
        params={'access_token': social.extra_data['access_token']}, data=json.dumps(announcements)
    )
    responsed = response.json()
    return responsed


# coursework
def getpostedcoursework(request,courseId):
    social = request.user.social_auth.get(provider='google-oauth2')
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/courseWork',
        params={'access_token': social.extra_data['access_token'],
                'courseWorkStates': 'PUBLISHED', 'orderBy': 'updateTime desc'}
    )
    postedcoursework = response.json().get('courseWork')
    return postedcoursework


def getStudentList(request,courseId):
    social = request.user.social_auth.get(provider='google-oauth2')
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/students',
        params={'access_token': social.extra_data['access_token']}
    )
    studentList = response.json().get('students')
    return studentList


def getStudentInfo(request,courseId,userId):
    social = request.user.social_auth.get(provider='google-oauth2')

    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/students/'+userId,
        params={'access_token': social.extra_data['access_token']}
    )
    studentInfo = response.json()
    return studentInfo

def getStudentAssignments(request,courseId,courseWorkId,userId):
    social = request.user.social_auth.get(provider='google-oauth2')

    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/courseWork/'+courseWorkId+'/studentSubmissions',
        params={'access_token': social.extra_data['access_token'],'userId':userId}
    )
    assignments = response.json().get('studentSubmissions')
    return assignments

#Late Submission tagging

def getSubmissionTime(request,courseId,userId):
    social = request.user.social_auth.get(provider='google-oauth2')
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/courseWork/-/studentSubmissions',
        params={'access_token': social.extra_data['access_token'],'userId':userId,'states':'TURNED_IN'}
    )
    submissionTime = response.json().get('studentSubmissions')
    return submissionTime

def getAssignmentwork(request,courseId,courseWorkId,submissionId):
    social = request.user.social_auth.get(provider='google-oauth2')
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/courseWork/'+courseWorkId+'/studentSubmissions/'+submissionId,
        params={'access_token': social.extra_data['access_token']}
    )
    assignmentWork = response.json()
    return assignmentWork

def createAssignmentwork(request,courseId,title,desc,maxPoint,links):
    social = request.user.social_auth.get(provider='google-oauth2')

    assignment = {
        "title": title,
        "description": desc,
        "materials": [],
        "maxPoints": maxPoint,
        "assigneeMode": "ALL_STUDENTS",
        "workType": "ASSIGNMENT",
        "state": "PUBLISHED",
        "submissionModificationMode": "MODIFIABLE",
    }
    if links :
        for link in links:
            lin = {"link":{"url":link}}
            assignment["materials"].append(dict(lin))

    response = requests.post(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/courseWork',
        params={'access_token': social.extra_data['access_token']},data=json.dumps(assignment)
    )
    
#plagiarism

# def plagiarism(request):
#    social = request.user.social_auth.get(provider='google-oauth2')
#    fileId = '1jHPHxzGzIxN9FIQalxe2As2XWXI-obkF'
#    response = requests.get(
#        'https://www.googleapis.com/drive/v3/files/'+fileId+'?alt=media',
#        params={'access_token': social.extra_data['access_token']}
#    )
#    fh = io.FileIO('test2.png', 'wb')
#    downloader = MediaIoBaseDownload(fh, response)
#    done = False
#    while done is False:
#        status, done = downloader.next_chunk()
