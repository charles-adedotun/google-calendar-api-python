from pydantic import BaseModel

class Appointment(BaseModel):
    attendee_email: str
    desired_start: str
    duration: int = 30
    meeting_title: str = "Meeting"
    meeting_description: str = "Meeting description"
    time_zone: str = "America/Chicago"
    event_id: str = None

class DeleteAppointment(BaseModel):
    event_id: str
