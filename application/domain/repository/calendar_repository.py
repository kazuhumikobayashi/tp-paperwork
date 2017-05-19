from datetime import date

from flask import current_app

from application.domain.model.holiday import Holiday
from application.domain.repository.google import calendar


class CalendarRepository(object):

    def find_holiday_by_year(self, year):
        google_calendar_api = calendar.get_calendar_api()

        # 祝日を取得する
        date_from = date(year=year, month=1, day=1).isoformat() + "T00:00:00.000000Z"
        date_to = date(year=year, month=12, day=31).isoformat() + "T00:00:00.000000Z"
        # API実行
        events_results = google_calendar_api.events().list(
            calendarId=calendar.JAPANESE_HOLIDAY_CALENDAR_ID,
            timeMin=date_from,
            timeMax=date_to,
            maxResults=50,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        # APIの実行結果からイベントを取り出す
        events = events_results.get('items', [])
        holidays = []
        for event in events:
            holidays.append(Holiday(event["start"]["date"], event["summary"]))
        current_app.logger.debug(holidays)
        return holidays
