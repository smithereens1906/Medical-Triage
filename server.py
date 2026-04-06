from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
from env.triage_env import TriageEnv

app = FastAPI()

env = TriageEnv()


class ActionRequest(BaseModel):
    action: str


@app.post("/reset")
async def reset():
    result = await env.reset()
    return result


@app.post("/step")
async def step(request: ActionRequest):
    result, reward, done, info = await env.step(request.action)
    return {
        "result": result,
        "reward": reward,
        "done": done,
        "info": info
    }