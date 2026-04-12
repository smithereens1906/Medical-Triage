from env.environment import HospitalTriageEnv
import json

env = HospitalTriageEnv()

# LOAD MODEL
try:
    with open("q_table.json", "r") as f:
        q_table_str = json.load(f)
        env.q_table = {eval(k): v for k, v in q_table_str.items()}
        print("Loaded trained model ✅")
except:
    print("No trained model found ⚠️ Run train.py first")

print("\n===== HOSPITAL TRIAGE SYSTEM =====\n")

name = input("Enter patient name: ")
age = int(input("Enter age: "))
gender = input("Enter gender: ")
symptoms = input("Enter symptoms: ")
arrival_type = input("Enter arrival type (walk-in / ambulance): ")

while True:
    try:
        duration = int(input("How many hours problem exists?: "))
        break
    except ValueError:
        print("Enter a valid number")

patient = {
    "name": name,
    "age": age,
    "gender": gender,
    "symptoms": symptoms,
    "arrival_type": arrival_type,
    "duration_hours": duration
}

state = env.reset(patient)

action = env.choose_action(state)

result, reward = env.step(patient, action)

print("\n--- TRIAGE RESULT ---\n")

print("Correct Department:", result["correct_department"])
print("AI Decision:", result["action"])
print("Urgency:", result["urgency"])
print("Redirected:", result["redirected"])
print("Reward:", reward)

# 🔥 SAVE UPDATED Q-TABLE (IMPORTANT)
q_table_str = {str(k): v for k, v in env.q_table.items()}

with open("q_table.json", "w") as f:
    json.dump(q_table_str, f, indent=4)

print("\nUpdated learning saved 💾")