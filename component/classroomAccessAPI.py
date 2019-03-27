import requests
import json

#Cousre
def cousreList(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses',
        params={'access_token': social.extra_data['access_token']}
    )
    listCourse = response.json().get('courses')
    return listCourse

#Announcment
def getAnnouncment(request):
    social = request.user.social_auth.get(provider='google-oauth2')
    courseId ='19606736198'
    response = requests.get(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/announcements',
        params={'access_token': social.extra_data['access_token'],'pageSize':2}
    )
    listAnnounce = response.json().get('announcements')
    return listAnnounce
def makeAnnouncment(request,textarea):
    social = request.user.social_auth.get(provider='google-oauth2')
    courseId ='19606736198'
    announcements = {
        "assigneeMode": "ALL_STUDENTS",
        "text": textarea,
        "state": "PUBLISHED"

    }
    response = requests.post(
        'https://classroom.googleapis.com/v1/courses/'+courseId+'/announcements',
        params={'access_token': social.extra_data['access_token']},data=json.dumps(announcements)
    )
    responsed = response.json()
    return responsed

 