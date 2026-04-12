from fastapi import FastAPI
from pydantic import BaseModel
from env.environment import TriageEnv

app = FastAPI()
env = TriageEnv()

class Patient(BaseModel):
    symptoms: str
    arrival_type: str
    age: int
    duration_hours: int

@app.post("/reset")
def reset(patient: Patient):
    state = env.reset(patient.dict())
    return {"state": state}

@app.post("/step")
def step(patient: Patient):

    state = env.get_state(patient.dict())
    action = env.choose_action(state)
    result, reward = env.step(patient.dict(), action)

    return {
        "result": result,
        "reward": reward
    }

@app.get("/")
def home():
    return {"message": "Medical Triage API is running 🚀"}