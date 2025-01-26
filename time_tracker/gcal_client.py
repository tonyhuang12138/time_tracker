from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os

SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class GoogleCalendarClient:
    def __init__(self):
        # Simple OAuth flow that opens browser for consent
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',
            SCOPES
        )
        creds = flow.run_local_server(port=0)
        self.service = build('calendar', 'v3', credentials=creds)
        
        # Find the Time Tracker calendar
        self.calendar_id = self._get_time_tracker_calendar()

    def _get_time_tracker_calendar(self):
        """Find the Time Tracker calendar ID"""
        calendar_list = self.service.calendarList().list().execute()
        for calendar in calendar_list['items']:
            if calendar['summary'] == 'Time Tracker':
                return calendar['id']
        raise ValueError("Could not find 'Time Tracker' calendar. Please create it in Google Calendar.")

    def get_events(self, days_back=7):
        """Fetch events from specified calendar for the last N days"""
        now = datetime.utcnow()
        start_time = (now - timedelta(days=days_back)).isoformat() + 'Z'
        
        events_result = self.service.events().list(
            calendarId=self.calendar_id,  # Use Time Tracker calendar
            timeMin=start_time,
            maxResults=1000,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', []) 