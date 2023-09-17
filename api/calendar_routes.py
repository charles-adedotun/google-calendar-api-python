from fastapi import APIRouter, HTTPException, Depends
from .models import Appointment
from .utils import book_appointment, update_appointment, delete_appointment
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

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

@router.put("/update-appointment/{event_id}/")
async def update_appointment_endpoint(event_id: str, appointment: Appointment, response: dict = Depends(handle_response)):
    return update_appointment(event_id, appointment.desired_start, appointment.duration, appointment.meeting_title, appointment.meeting_description, appointment.time_zone)

@router.delete("/delete-appointment/{event_id}/")
async def delete_appointment_endpoint(event_id: str, response: dict = Depends(handle_response)):
    return delete_appointment(event_id)
