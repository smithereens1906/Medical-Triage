from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict
from env.environment import TriageEnv

app = FastAPI()
env = TriageEnv()

class Patient(BaseModel):
    symptoms: str
    arrival_type: str
    age: int
    duration_hours: int

# ✅ FIXED RESET (handles empty body from OpenEnv)
@app.post("/reset")
def reset(patient: Optional[Dict] = None):

    if patient is None:
        # default fallback (required for OpenEnv)
        patient = {
            "symptoms": "fever",
            "arrival_type": "walk-in",
            "age": 30,
            "duration_hours": 2
        }

    state = env.reset(patient)
    return {"state": state}

# ✅ STEP endpoint
@app.post("/step")
def step(patient: Patient):

    patient_dict = patient.dict()

    state = env.get_state(patient_dict)
    action = env.choose_action(state)
    result, reward = env.step(patient_dict, action)

    return {
        "result": result,
        "reward": reward
    }

# ✅ Health check
@app.get("/")
def home():
    return {"message": "Medical Triage API is running 🚀"}