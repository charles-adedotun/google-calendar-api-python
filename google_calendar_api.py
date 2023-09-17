import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load credentials
with open('credentials.json', 'r') as f:
    creds_data = json.load(f)

# Impersonate user
SUBJECT_EMAIL = 'charles@tryneublink.com'
creds = Credentials.from_service_account_info(creds_data, scopes=[
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events'
], subject=SUBJECT_EMAIL)

service = build('calendar', 'v3', credentials=creds)

def create_calendar(calendar_title):
    try:
        calendar = {
            'summary': calendar_title,
            'timeZone': 'UTC'
        }
        created_calendar = service.calendars().insert(body=calendar).execute()
        return created_calendar['id']
    except HttpError as e:
        raise Exception(f"Could not create calendar: {e}")

def schedule_meeting(calendar_id, meeting_title, meeting_description, start_date, end_date, time_zone, attendee_email):
    try:
        event = {
            'summary': meeting_title,
            'description': meeting_description,
            'start': {
                'dateTime': start_date,
                'timeZone': time_zone,
            },
            'end': {
                'dateTime': end_date,
                'timeZone': time_zone,
            },
            'reminders': {
                'useDefault': True,
            },
            'attendees': [{'email': attendee_email}],
            'sendUpdates': 'all',
        }
        return service.events().insert(calendarId=calendar_id, body=event).execute()
    except HttpError as e:
        raise Exception(f"Could not create event: {e}")
