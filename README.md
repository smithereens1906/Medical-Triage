---
title: Medical Triage System
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
---
# 🏥 Medical Appointment Triage System

## 📌 Overview
This project simulates a real-world hospital triage system where patients are assigned to departments, prioritized based on urgency, and managed under resource constraints.

The system uses a simulation environment and decision logic to optimize patient handling and maximize efficiency.

---

## 🚀 Features

### ✅ Core Features
- Department Routing (symptoms → correct department)
- Urgency Scoring (1–100 scale)
- Doctor Assignment (limited availability)
- Priority Scheduling

### 🔥 Advanced Features
- Ambulance Priority System 🚑
- Resource Constraints (ICU beds, doctors)
- Patient Redirection (when resources unavailable)
- Simulation Engine (multiple patients)

---

## 🧠 How It Works

1. A patient is generated with:
   - Symptoms
   - Urgency level
   - Arrival type (walk-in / ambulance)

2. The system:
   - Routes patient to correct department
   - Assigns available resources
   - Applies priority logic (urgency + ambulance)

3. If resources are unavailable:
   - Patient is redirected

---

## 📊 Scoring System

### ✅ Rewards:
- Correct department assignment (+1)
- High urgency handling (>70) (+1)
- Ambulance priority (+1)
- ICU allocation for critical cases (+1)

### ❌ Penalties:
- Wrong department (-1)
- No available doctor (-1)
- ICU unavailable for critical patient (-1)

### 📈 Final Score:
- Normalized between **0 and 1**
- Formula: