import asyncio
from env.environment import TriageEnv

async def run():
    env = TriageEnv()

    print("[START]")

    # 🔥 FULL USER INPUT
    name = input("Enter patient name: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender (male/female): ")
    symptoms = input("Enter symptoms: ")
    arrival = input("Enter arrival type (walk-in / ambulance): ")

    # ❌ NO manual urgency (auto-calculated)
    patient = {
        "name": name,
        "age": age,
        "gender": gender,
        "symptoms": symptoms,
        "arrival_type": arrival
    }

    state = await env.reset(patient)

    print("[STEP] Initial State:", state)

    # 🔥 smarter decision logic
    symptom_map = env.symptom_map
    action = symptom_map.get(symptoms.lower(), "General Medicine")

    result, reward, done, _ = await env.step(action)

    print("[STEP] Action:", action)
    print("[STEP] Result:", result)
    print("[STEP] Reward:", reward)

    print("[END]")

if __name__ == "__main__":
    asyncio.run(run())