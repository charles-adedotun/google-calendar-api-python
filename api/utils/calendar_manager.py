from services.google_calendar import (
    get_existing_event_for_attendee, get_available_slots, schedule_meeting,
    get_overlapping_events, update_appointment, delete_appointment
)
from .time_helpers import get_utc_time, convert_to_timezone
import datetime
from config import CALENDAR_ID

def book_appointment(attendee_email: str, desired_start: str, duration: int = 30, meeting_title: str = "Meeting", meeting_description: str = "Description", time_zone: str = "America/Chicago"):
    existing_event = get_existing_event_for_attendee(CALENDAR_ID, attendee_email)
    if existing_event:
        return f"Existing event found: {existing_event['id']}"
    
    local_desired_start = convert_to_timezone(desired_start, time_zone)
    desired_start_utc = get_utc_time(local_desired_start)
    desired_end_utc = get_utc_time((datetime.datetime.fromisoformat(local_desired_start) + datetime.timedelta(minutes=duration)).isoformat())

    # Check for overlapping events
    overlapping_events = get_overlapping_events(CALENDAR_ID, desired_start, desired_end_utc)

    if overlapping_events:
        available_slots = get_available_slots(CALENDAR_ID, desired_start, duration)
        return f"Desired time is not available. Here are the available slots: {available_slots}"
    else:
        event = schedule_meeting(
            CALENDAR_ID,
            "Meeting",
            "Description",
            desired_start_utc,
            desired_end_utc,
            time_zone,
            attendee_email
        )
        return event

def update_appointment_util(event_id: str, new_start: str, duration: int, meeting_title: str, meeting_description: str, time_zone: str = "America/Chicago"):
    try:
        response = update_appointment(CALENDAR_ID, event_id, new_start, duration, meeting_title, meeting_description, time_zone)
        return response

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

def delete_appointment_util(event_id: str):
    try:
        response = delete_appointment(CALENDAR_ID, event_id)
        return response

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
