import os
import json
from google_calendar_api import create_calendar, schedule_meeting
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load from environment or .env
CALENDAR_ID = os.environ.get('CALENDAR_ID')

if not CALENDAR_ID:
    CALENDAR_ID = create_calendar("Schedule Bot Test")
    print(f"Calendar created with ID: {CALENDAR_ID}")
else:
    print(f"Using existing calendar with ID: {CALENDAR_ID}")

event = schedule_meeting(
    CALENDAR_ID,
    "Team Meeting",
    "Discuss project updates",
    "2023-09-14T10:00:00",
    "2023-09-14T11:00:00",
    "America/Los_Angeles",
    "attendee@example.com"
)

print(f"Event created successfully: {event['htmlLink']}")
