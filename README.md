---
title: Medical Triage System
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---

# 🏥 Medical Triage System

## 📌 Overview
This project simulates a hospital triage system using reinforcement learning.  
Patients are assigned to appropriate departments based on symptoms, urgency, and arrival type.

---

## 🚀 Features

- Department Routing (symptoms → correct department)
- Urgency Scoring (based on age, arrival type, duration)
- Reinforcement Learning (Q-learning)
- Adaptive decision-making (improves over time)

---

## 🧠 How It Works

1. Patient data is input:
   - Symptoms
   - Arrival type
   - Age
   - Duration

2. The system:
   - Computes urgency
   - Selects department using Q-learning
   - Updates Q-values based on reward

---

## 📊 Reward System

- Correct decision → positive reward
- Wrong decision → negative reward
- High urgency handled → bonus reward

---
