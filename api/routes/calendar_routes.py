from fastapi import APIRouter, HTTPException
from ..models import Appointment, DeleteAppointment
from api.utils.calendar_manager import book_appointment, update_appointment_util, delete_appointment_util
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
