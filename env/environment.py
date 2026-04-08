import random

class TriageEnv:
    def __init__(self):
        self.available_doctors = 3
        self.available_icu = 2
        self.patient = None
        self.done = False

        # 🔥 Priority queue
        self.queue = []

        # Symptom → Department mapping
        self.symptom_map = {
            "chest pain": "Cardiology",
            "shortness of breath": "Cardiology",
            "irregular heartbeat": "Cardiology",
            "palpitations": "Cardiology",
            "sudden high blood pressure": "Cardiology",

            "breathing difficulty": "Respiratory",
            "persistent cough": "Respiratory",
            "wheezing": "Respiratory",
            "asthma attack": "Respiratory",
            "coughing blood": "Respiratory",

            "severe headache": "Neurology",
            "dizziness": "Neurology",
            "fainting": "Neurology",
            "seizures": "Neurology",
            "slurred speech": "Neurology",

            "fever": "General Medicine",
            "vomiting": "General Medicine",
            "nausea": "General Medicine",
            "fatigue": "General Medicine",
            "dehydration": "General Medicine",

            "severe stomach pain": "Gastrointestinal",
            "diarrhea": "Gastrointestinal",
            "blood in stool": "Gastrointestinal",
            "loss of appetite": "Gastrointestinal",

            "fracture": "Orthopedics",
            "severe bleeding": "Orthopedics",
            "back pain": "Orthopedics",
            "joint swelling": "Orthopedics",

            "unconscious patient": "Emergency",
            "severe allergic reaction": "Emergency"
        }

        self.symptoms_list = list(self.symptom_map.keys())

    # 🔥 urgency logic
    def calculate_urgency(self, age, symptoms, arrival):
        urgency = 30

        critical = ["unconscious patient", "seizures", "coughing blood", "severe allergic reaction"]
        if symptoms in critical:
            urgency += 50

        if age > 60:
            urgency += 20
        elif age < 10:
            urgency += 15

        if arrival == "ambulance":
            urgency += 20

        return min(urgency, 100)

    async def reset(self, patient_data=None):
        self.done = False

        # Generate or use input
        if patient_data:
            if "urgency" not in patient_data:
                patient_data["urgency"] = self.calculate_urgency(
                    patient_data["age"],
                    patient_data["symptoms"],
                    patient_data["arrival_type"]
                )
            self.patient = patient_data
        else:
            symptom = random.choice(self.symptoms_list)
            age = random.randint(1, 90)
            arrival = random.choice(["walk-in", "ambulance"])

            self.patient = {
                "name": "Unknown",
                "age": age,
                "gender": random.choice(["male", "female"]),
                "symptoms": symptom,
                "arrival_type": arrival,
                "urgency": self.calculate_urgency(age, symptom, arrival)
            }

        # 🔥 Add to priority queue
        self.queue.append(self.patient)
        self.queue.sort(key=lambda x: x["urgency"], reverse=True)

        position = self.queue.index(self.patient) + 1

        return {
            "patient": self.patient,
            "queue_position": position,
            "patients_waiting": len(self.queue) - 1
        }

    def route_department(self, symptoms):
        return self.symptom_map.get(symptoms.lower(), "General Medicine")

    async def step(self, action):
        if self.done:
            return {}, 0, True, {}

        correct_department = self.route_department(self.patient["symptoms"])
        urgency = self.patient["urgency"]
        arrival = self.patient["arrival_type"]

        reward = 0
        redirected = False

        # correct routing
        if action == correct_department:
            reward += 1
        else:
            reward -= 1

        # urgency bonus
        if urgency > 70:
            reward += 1

        # ambulance bonus
        if arrival == "ambulance":
            reward += 1

        # ICU logic
        if urgency > 80:
            if self.available_icu > 0:
                self.available_icu -= 1
                reward += 1
            else:
                redirected = True
                reward -= 1

        # 🔥 Priority queue processing
        if self.available_doctors > 0 and len(self.queue) > 0:
            self.available_doctors -= 1
            served_patient = self.queue.pop(0)

            if served_patient == self.patient:
                reward += 1
            else:
                reward -= 2  # penalty for bad prioritization

        else:
            redirected = True
            reward -= 1

        self.done = True

        return {
            "patient": self.patient,
            "correct_department": correct_department,
            "action": action,
            "urgency": urgency,
            "arrival_type": arrival,
            "queue_length": len(self.queue),
            "available_doctors": self.available_doctors,
            "available_icu": self.available_icu,
            "redirected": redirected
        }, reward, self.done, {}

    async def get_state(self):
        return {
            "current_patient": self.patient,
            "queue_length": len(self.queue),
            "queue": self.queue
        }

    async def close(self):
        pass