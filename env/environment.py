import random

class HospitalTriageEnv:

    def __init__(self):

        self.departments = [
            "Cardiology",
            "Respiratory",
            "Neurology",
            "General Medicine",
            "Gastrointestinal",
            "Orthopedics",
            "Emergency"
        ]

        # KEEP SIMPLE (NO NORMALIZATION NOW)
        self.symptom_department = {
            "chest pain": "Cardiology",
            "breathing difficulty": "Respiratory",
            "severe headache": "Neurology",
            "fever": "General Medicine",
            "gas": "Gastrointestinal",
            "fracture": "Orthopedics",
            "unconscious patient": "Emergency"
        }

        self.q_table = {}

        self.alpha = 0.3
        self.epsilon = 0.05

    # -------------------------
    def get_state(self, patient):
        return (patient["symptoms"], patient["arrival_type"])

    # -------------------------
    def choose_action(self, state):

        if random.uniform(0,1) < self.epsilon:
            return random.choice(self.departments)

        if state not in self.q_table:
            self.q_table[state] = {d: 0 for d in self.departments}

        return max(self.q_table[state], key=self.q_table[state].get)

    # -------------------------
    def calculate_urgency(self, patient):

        urgency = 20

        if patient["arrival_type"] == "ambulance":
            urgency += 30

        if patient["age"] > 60:
            urgency += 10

        if patient["duration_hours"] < 1:
            urgency += 20

        return urgency

    # -------------------------
    def reset(self, patient):
        patient["urgency"] = self.calculate_urgency(patient)
        return self.get_state(patient)

    # -------------------------
    def step(self, patient, action):

        correct_department = self.symptom_department.get(
            patient["symptoms"],
            "General Medicine"
        )

        # safety override
        if patient["urgency"] > 70:
            action = correct_department

        reward = 0
        redirected = False

        if action == correct_department:
            reward += 10
        else:
            redirected = True
            reward -= 10

        state = self.get_state(patient)

        if state not in self.q_table:
            self.q_table[state] = {d: 0 for d in self.departments}

        old_value = self.q_table[state][action]

        # STRONG UPDATE
        if action == correct_department:
            new_value = old_value + self.alpha * (reward) + 2
        else:
            new_value = old_value + self.alpha * (reward) - 2

        self.q_table[state][action] = new_value

        result = {
            "correct_department": correct_department,
            "action": action,
            "urgency": patient["urgency"],
            "redirected": redirected
        }

        return result, reward