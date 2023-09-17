from pydantic import BaseModel

class Appointment(BaseModel):
    attendee_email: str
    desired_start: str
    duration: int = 30
    meeting_title: str = None
    meeting_description: str = None
    time_zone: str = "America/Chicago"
