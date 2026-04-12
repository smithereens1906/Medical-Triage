from env.environment import HospitalTriageEnv
import json

env = HospitalTriageEnv()

# LOAD MODEL
try:
    with open("q_table.json", "r") as f:
        q_table_str = json.load(f)
        env.q_table = {eval(k): v for k, v in q_table_str.items()}
except:
    print("No trained model found ⚠️")

print("[START]")

patient = {
    "symptoms": "chest pain",
    "arrival_type": "ambulance",
    "age": 65,
    "duration_hours": 1
}

print(f"[STEP] Input: {patient}")

state = env.reset(patient)
action = env.choose_action(state)
result, reward = env.step(patient, action)

print(f"[STEP] Decision: {result['action']}")
print(f"[STEP] Reward: {reward}")

print("[END]")