import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

GCREDS_FILE = 'client_secret_334864306014-l9s3jg2fir3r29hndd6li6jg058rfche.apps.googleusercontent.com.json'


def authenticate_google():
    # Load credentials from file
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        GCREDS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    service = googleapiclient.discovery.build('photoslibrary', 'v1', credentials=credentials)
    return service

def list_photos(service):
    results = service.mediaItems().list(pageSize=100).execute()
    items = results.get('mediaItems', [])
    
    while 'nextPageToken' in results:
        results = service.mediaItems().list(pageSize=100, pageToken=results['nextPageToken']).execute()
        items.extend(results.get('mediaItems', []))


def main():
    service = authenticate_google()
    photos = list_photos(service)
    for photo in photos:
        print(photo['filename'])

if __name__ == '__main__':
    main()
    
