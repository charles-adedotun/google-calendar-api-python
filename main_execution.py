import os
from google_calendar_api import get_existing_event_for_attendee, get_available_slots, schedule_meeting, get_overlapping_events
from dotenv import load_dotenv
import datetime

# Load environment variables from .env file
load_dotenv()

# Load from environment or .env
CALENDAR_ID = os.environ.get('CALENDAR_ID')
if not CALENDAR_ID:
    raise Exception("Please set the CALENDAR_ID environment variable.")

def book_or_suggest_appointment(attendee_email, desired_start, duration):
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

# # Use the function
# attendee_email = input("Enter the attendee's email address: ")
# desired_start = input("Enter the desired start time (e.g., 2023-09-14T10:00:00): ")
# duration = int(input("Enter the duration of the meeting in minutes: "))

# Test the function
attendee_email = "attendee-6@example.com"
desired_start = "2023-09-17T10:00:00"
duration = int(60)

desired_start = desired_start if desired_start.endswith('Z') else desired_start + 'Z'

result = book_or_suggest_appointment(attendee_email, desired_start, duration)
print(result)
