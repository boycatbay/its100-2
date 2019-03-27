from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students']

def courseworkList():
    creds = None
   # The file token.pickle stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
    if os.path.exists('token_cw.pickle'):
        with open('token_cw.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token_cw.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    courseworkList = service.courses().courseWork().studentSubmissions().list(
        courseId='19606736198',courseWorkId='32978353514',userId='107235148265490091119').execute()
    courseworkList = courseworkList.get('studentSubmissions')
    return courseworkList
if __name__ == '__main__':
    coursework = courseworkList()
    print(coursework)
   # textarea = "test"
   # material = "-"
   # postAnum(textarea,material)

    
