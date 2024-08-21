import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
from datetime import datetime, timedelta, timezone


SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

GCREDS_FILE = 'client_secret_334864306014-l9s3jg2fir3r29hndd6li6jg058rfche.apps.googleusercontent.com.json'


def authenticate_google():
    # Load credentials from file
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        GCREDS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    service = googleapiclient.discovery.build('photoslibrary', 'v1', credentials=credentials, static_discovery=False)
    return service

def parse_creation_time(creation_time_str):
    try:
        return datetime.strptime(creation_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        return datetime.strptime(creation_time_str, '%Y-%m-%dT%H:%M:%S%z')

def list_photos(service, cutoff_date=(datetime.now(timezone.utc) - timedelta(days=365)).strftime('%Y-%m-%d')):
    results = service.mediaItems().list(pageSize=100).execute()
    items = results.get('mediaItems', [])
    
    while 'nextPageToken' in results:
        results = service.mediaItems().list(pageSize=100, pageToken=results['nextPageToken']).execute()
        items.extend(results.get('mediaItems', []))

    cutoff_datetime = datetime.strptime(cutoff_date, '%Y-%m-%d').replace(tzinfo=timezone.utc)
    filtered_items = [item for item in items if 'mediaMetadata' in item and 'creationTime' in item['mediaMetadata'] and parse_creation_time(item['mediaMetadata']['creationTime']) < cutoff_datetime]

    return filtered_items


def main():
    service = authenticate_google()
    photos = list_photos(service)
    for photo in photos:
        print(photo['creationTime'])

if __name__ == '__main__':
    main()
    
