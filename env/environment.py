import random

class TriageEnv:
    def __init__(self):
        self.available_doctors = 3
        self.available_icu = 2
        self.patient = None
        self.done = False

    async def reset(self):
        self.available_doctors = 3
        self.available_icu = 2
        self.done = False

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
        return "General Medicine"

    async def step(self, action):
        if self.done:
            return {}, 0, True, {}

        correct_department = self.route_department(self.patient["symptoms"])
        urgency = self.patient["urgency"]
        arrival = self.patient["arrival_type"]

        reward = 0
        redirected = False

        if action == correct_department:
            reward += 1
        else:
            reward -= 1

        if urgency > 70:
            reward += 1

        if arrival == "ambulance":
            reward += 1

        if urgency > 80:
            if self.available_icu > 0:
                self.available_icu -= 1
                reward += 1
            else:
                redirected = True
                reward -= 1

        if self.available_doctors > 0:
            self.available_doctors -= 1
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
            "available_doctors": self.available_doctors,
            "available_icu": self.available_icu,
            "redirected": redirected
        }, reward, self.done, {}

    async def get_state(self):
        return self.patient

    async def close(self):
        pass