import apiclient
from flask import current_app
from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
JAPANESE_HOLIDAY_CALENDAR_ID = "ja.japanese#holiday@group.v.calendar.google.com"


def _get_credentials():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(current_app.config['CLIENT_SECRET_FILE'], SCOPES)
    return credentials


def get_calendar_api():
    # 認証情報作成
    credentials = _get_credentials()
    http_auth = credentials.authorize(Http())
    # API利用できる状態を作る
    api = apiclient.discovery.build("calendar", "v3", http=http_auth)
    return api
