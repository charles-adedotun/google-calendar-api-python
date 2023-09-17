from google_calendar_api import get_existing_event_for_attendee, get_available_slots, schedule_meeting, get_overlapping_events
import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load from environment or .env
CALENDAR_ID = os.environ.get('CALENDAR_ID')
if not CALENDAR_ID:
    raise Exception("Please set the CALENDAR_ID environment variable.")

def book_appointment(attendee_email: str, desired_start: str, duration: int = 30, meeting_title: str = "Meeting", meeting_description: str = "Description", time_zone: str = "America/Chicago"):
    existing_event = get_existing_event_for_attendee(CALENDAR_ID, attendee_email)
    if existing_event:
        return f"Existing event found: {existing_event['htmlLink']}"
    
    desired_end = (datetime.datetime.strptime(desired_start, "%Y-%m-%dT%H:%M:%SZ") + datetime.timedelta(minutes=duration)).isoformat() + 'Z'

    # Check for overlapping events
    overlapping_events = get_overlapping_events(CALENDAR_ID, desired_start, desired_end)

    if overlapping_events:
        available_slots = get_available_slots(CALENDAR_ID, desired_start, duration)
        return f"Desired time is not available. Here are the available slots: {available_slots}"
    else:
        event = schedule_meeting(
            CALENDAR_ID,
            "Meeting",
            "Description",
            desired_start,
            desired_end,
            "America/Los_Angeles",
            attendee_email
        )
        return f"Event created successfully: {event['htmlLink']}"

def update_appointment(event_id: str, new_start: str, duration: int, meeting_title: str, meeting_description: str, time_zone: str):
  print("update appointment")

def delete_appointment(event_id: str):
    print("delete appointment")
