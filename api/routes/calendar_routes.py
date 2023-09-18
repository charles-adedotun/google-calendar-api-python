from fastapi import APIRouter, HTTPException
from typing import List
from api.models import Appointment, DeleteAppointment
from api.utils.calendar_manager import book_appointment, update_appointment_util, delete_appointment_util, get_upcoming
from config import CALENDAR_ID

router = APIRouter()

def handle_response(response: dict = None):
    if response and response.get('status') == 'error':
        raise HTTPException(status_code=400, detail=response.get('message'))
    return response

@router.post("/create-appointment/")
async def create_appointment(appointment: Appointment):
    return book_appointment(
        appointment.attendee_email,
        appointment.desired_start,
        appointment.duration,
        appointment.meeting_title,
        appointment.meeting_description,
        appointment.time_zone
    )

@router.put("/update-appointment/")
async def update_appointment_endpoint(appointment: Appointment):
    return update_appointment_util(
        appointment.event_id,
        appointment.desired_start,
        appointment.duration,
        appointment.meeting_title,
        appointment.meeting_description,
        appointment.time_zone
    )

@router.delete("/delete-appointment/")
async def delete_appointment_endpoint(appointment: DeleteAppointment):
    return delete_appointment_util(appointment.event_id)

@router.get("/upcoming-events/")
async def get_upcoming_events(max_results: int = 3):
    try:
        upcoming_events = get_upcoming(max_results)
        return upcoming_events
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
