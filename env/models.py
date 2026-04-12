from pydantic import BaseModel

class Patient(BaseModel):
    symptoms: str
    arrival_type: str
    age: int
    duration_hours: int