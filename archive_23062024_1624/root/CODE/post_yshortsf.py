import httplib2
import os
import random
import sys
import time
from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from google.oauth2.credentials import Credentials



YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def post_yshorts(file_path, title, keywords="", privacy_status="public"):
    credentials = Credentials.from_authorized_user_file('credentials.json', scopes=[YOUTUBE_UPLOAD_SCOPE])
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, credentials=credentials)

    body = {
        'snippet': {
            'title': title,
            'tags': keywords.split(","),
            'categoryId': '17'  
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(file_path, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)



# Реализация метода обратного вызова для перезапуска загрузки при ошибке
def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    pass
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status, e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            retry += 1
            if retry > MAX_RETRIES:
                exit("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            time.sleep(sleep_seconds)
