from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
SCOPES = ['https://www.googleapis.com/auth/classroom.profile.emails','https://www.googleapis.com/auth/classroom.rosters','https://www.googleapis.com/auth/classroom.profile.photos']

def studentMail(UserId): 
    creds = None
   # The file token.pickle stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
    if os.path.exists("token_roaster.pickle"):
        with open('token_roaster.pickle', 'rb') as token:
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
        with open('token_roaster.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('classroom', 'v1', credentials=creds)
    studentMail = service.userProfiles().get(userId=UserId).execute()
    return studentMail

if __name__ == '__main__':
    studentMail = studentMail(107235148265490091119)
    print(studentMail)