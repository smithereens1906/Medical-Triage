from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Dict
from env.environment import TriageEnv

app = FastAPI()

env = TriageEnv()


class ActionRequest(BaseModel):
    action: str


@app.post("/reset")
async def reset(patient: Optional[Dict] = None):
    return await env.reset(patient)


@app.post("/step")
async def step(request: ActionRequest):
    result, reward, done, info = await env.step(request.action)
    return {
        "result": result,
        "reward": reward,
        "done": done,
        "info": info
    }


@app.get("/state")
async def state():
    return await env.get_state()
@app.get("/")
def home():
    return {"message": "Medical Triage API is running 🚀"}