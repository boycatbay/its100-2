from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/drive.appdata','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive.metadata']

def courseworkList():
    creds = None
   # The file token.pickle stores the user's access and refresh tokens, and is
   # created automatically when the authorization flow completes for the first
   # time.
    if os.path.exists('token_d.pickle'):
        with open('token_d.pickle', 'rb') as token:
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
        with open('token_d.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    courseworkList = service.files().list(
          pageSize=10).execute()
    return courseworkList
if __name__ == '__main__':
    coursework = courseworkList()
    print(coursework)
   # textarea = "test"
   # material = "-"
   # postAnum(textarea,material)

    
