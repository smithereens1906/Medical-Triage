import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:7860")
MODEL_NAME = os.getenv("MODEL_NAME", "dummy-model")
HF_TOKEN = os.getenv("HF_TOKEN")
import asyncio
from env.environment import TriageEnv

async def run():

    env = TriageEnv()

    print("[START]")

    # 🔥 Take user input
    symptoms = input("Enter symptoms (chest pain / fever / injury): ")
    urgency = int(input("Enter urgency (1-100): "))
    arrival = input("Enter arrival type (walk-in / ambulance): ")

    patient = {
        "symptoms": symptoms,
        "urgency": urgency,
        "arrival_type": arrival
    }

    state = await env.reset(patient)

    print("[STEP] Initial State:", state)

    # simple decision logic
    if symptoms == "chest pain":
        action = "Cardiology"
    elif symptoms == "fever":
        action = "General Medicine"
    else:
        action = "Orthopedics"

    result, reward, done, _ = await env.step(action)

    print("[STEP] Action:", action)
    print("[STEP] Result:", result)
    print("[STEP] Reward:", reward)

    print("[END]")

if __name__ == "__main__":
    asyncio.run(run())