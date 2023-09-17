import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import pytz

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

def is_overlapping(event1_start, event1_end, event2_start, event2_end):
    return (event1_start < event2_end) and (event1_end > event2_start)

def get_existing_event_for_attendee(calendar_id, attendee_email):
    try:
        events = service.events().list(calendarId=calendar_id, q=attendee_email, singleEvents=True).execute().get('items', [])
        for event in events:
            attendees = [a['email'] for a in event.get('attendees', [])]
            if attendee_email in attendees:
                return event
        return None
    except HttpError as e:
        raise Exception(f"Error fetching events for attendee: {e}")

def get_overlapping_events(calendar_id, desired_start, desired_end):
    try:
        # Ensure timestamps are in RFC3339 format
        desired_start = desired_start.replace('+00:00', '') + ('' if desired_start.endswith('Z') else 'Z')
        desired_end = desired_end.replace('+00:00', '') + ('' if desired_end.endswith('Z') else 'Z')

        all_events = service.events().list(
            calendarId=calendar_id,
            timeMin=desired_start,
            timeMax=desired_end,
            singleEvents=True
        ).execute().get('items', [])

        # Filter out non-overlapping events
        overlapping_events = [event for event in all_events if is_overlapping(desired_start, desired_end, event['start'].get('dateTime'), event['end'].get('dateTime'))]
        
        return overlapping_events
    except HttpError as e:
        raise Exception(f"Error fetching overlapping events: {e}")

def get_available_slots(calendar_id, desired_start, duration, num_slots=3):
    end_of_day = "18:00:00"  # 6 PM
    start_time_obj = datetime.fromisoformat(desired_start)
    end_of_day_obj = datetime.combine(start_time_obj.date(), datetime.strptime(end_of_day, "%H:%M:%S").time())
    current_time = current_time = datetime.strptime(desired_start, "%Y-%m-%dT%H:%M:%SZ")

    # Localize datetime objects to UTC timezone
    utc = pytz.UTC
    current_time = current_time.replace(tzinfo=utc)
    end_of_day_obj = end_of_day_obj.replace(tzinfo=utc)
    
    available_slots = []
    current_time = start_time_obj
    while current_time + timedelta(minutes=duration) <= end_of_day_obj and len(available_slots) < num_slots:
        potential_end_time = current_time + timedelta(minutes=duration)
        conflicting_events = get_overlapping_events(calendar_id, current_time.isoformat(), potential_end_time.isoformat())

        if not conflicting_events:
            available_slots.append((current_time, potential_end_time))
        current_time = current_time + timedelta(minutes=30)  # Check every 30 minutes
        
    return [slot[0].strftime('%Y-%m-%dT%H:%M:%SZ') for slot in available_slots]

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
