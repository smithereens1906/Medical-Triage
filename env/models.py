from pydantic import BaseModel

class Patient(BaseModel):
    symptoms: str
    urgency: int
    arrival_type: str