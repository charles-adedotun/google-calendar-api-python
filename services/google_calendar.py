from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import pytz
from config import logger, SUBJECT_EMAIL, creds_data
from api.utils.time_helpers import convert_to_timezone, get_utc_time

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
        # Convert the start_date and end_date to the appropriate timezone format
        start_date_local = convert_to_timezone(start_date, time_zone)
        end_date_local = convert_to_timezone(end_date, time_zone)

        event = {
            'summary': meeting_title,
            'description': meeting_description,
            'start': {
                'dateTime': start_date_local,
                'timeZone': time_zone,
            },
            'end': {
                'dateTime': end_date_local,
                'timeZone': time_zone,
            },
            'reminders': {
                'useDefault': True,
            },
            'attendees': [{'email': attendee_email}],
            'sendUpdates': 'all',
        }
        created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
        
        # Log the event creation
        logger.info(f"Created event with ID: {created_event['id']}")

        return created_event

    except HttpError as e:
        raise Exception(f"Could not create event: {e}")

def update_appointment(calendar_id, event_id, new_start, duration, meeting_title, meeting_description, time_zone):
    try:
        # Fetch the existing event
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

        # Update the event details
        new_start_local = convert_to_timezone(new_start, time_zone)
        new_end = (datetime.fromisoformat(new_start) + timedelta(minutes=duration)).isoformat()
        new_end_local = convert_to_timezone(new_end, time_zone)

        event['start']['dateTime'] = new_start_local
        event['end']['dateTime'] = new_end_local
        event['start']['timeZone'] = time_zone
        event['end']['timeZone'] = time_zone
        event['summary'] = meeting_title
        event['description'] = meeting_description

        # Use the API to update the event
        updated_event = service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()

        # Log the event update
        logger.info(f"Updated event with ID: {updated_event['id']}")

        return updated_event

    except HttpError as e:
        raise Exception(f"Could not update event: {e}")

def delete_appointment(calendar_id, event_id):
    try:
        # Delete the event
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()

        # Return a confirmation message and the ID of the deleted event
        return {
            "message": "Event deleted successfully.",
            "event_id": event_id
        }

    except HttpError as e:
        raise Exception(f"Could not delete event: {e}")

def get_upcoming_events(calendar_id, max_results):
    try:
        # Get current time in RFC3339 format
        now = datetime.utcnow().isoformat() + 'Z'

        # Fetch upcoming events after the current time
        events_result = service.events().list(calendarId=calendar_id, timeMin=now, maxResults=max_results, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        # Return the fetched events
        return events

    except HttpError as e:
        raise Exception(f"Could not fetch upcoming events: {e}")
