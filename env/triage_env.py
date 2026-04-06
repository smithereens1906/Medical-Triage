import random

class TriageEnv:
    def __init__(self):
        self.available_doctors = 3
        self.available_icu = 2

    async def reset(self):
        self.patient = {
            "symptoms": random.choice(["chest pain", "fever", "injury"]),
            "urgency": random.randint(1, 100),
            "arrival_type": random.choice(["walk-in", "ambulance"])
        }

        return self.patient

    def route_department(self, symptoms):
        if symptoms == "chest pain":
            return "Cardiology"
        elif symptoms == "fever":
            return "General Medicine"
        elif symptoms == "injury":
            return "Orthopedics"
        else:
            return "General Medicine"

    async def step(self, action):
        correct_department = self.route_department(self.patient["symptoms"])
        urgency = self.patient["urgency"]
        arrival = self.patient["arrival_type"]

        reward = 0
        redirected = False

        # correct department
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

        # 🏥 ICU logic
        if urgency > 80:
            if self.available_icu > 0:
                self.available_icu -= 1
                reward += 1
            else:
                redirected = True
                reward -= 1  # couldn’t handle critical case

        # 👨‍⚕️ doctor logic
        if self.available_doctors > 0:
            self.available_doctors -= 1
        else:
            redirected = True
            reward -= 1

        done = True

        return {
            "patient": self.patient,
            "correct_department": correct_department,
            "urgency": urgency,
            "arrival_type": arrival,
            "available_doctors": self.available_doctors,
            "available_icu": self.available_icu,
            "redirected": redirected  # NEW
        }, reward, done, {}

    async def close(self):
        pass