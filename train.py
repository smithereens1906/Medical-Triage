from env.environment import HospitalTriageEnv
import random
import json

env = HospitalTriageEnv()

symptoms_list = list(env.symptom_department.keys())
arrival_types = ["walk-in", "ambulance"]

print("Training started...\n")

for _ in range(5000):

    symptom = random.choice(symptoms_list)

    patient = {
        "symptoms": symptom,
        "arrival_type": random.choice(arrival_types),
        "age": random.randint(10, 80),
        "duration_hours": random.randint(0, 10)
    }

    state = env.reset(patient)

    if random.uniform(0,1) < 0.8:
        action = env.symptom_department[symptom]
    else:
        action = env.choose_action(state)

    result, reward = env.step(patient, action)

print("\nTraining Done ✅")

q_table_str = {str(k): v for k, v in env.q_table.items()}

with open("q_table.json", "w") as f:
    json.dump(q_table_str, f, indent=4)

print("Q-table saved 💾")