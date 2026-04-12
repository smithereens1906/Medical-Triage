import yaml
import importlib

print("🔍 Loading openenv.yaml...")

with open("openenv.yaml", "r") as f:
    config = yaml.safe_load(f)

env_file = config["environment"]["file"].replace(".py", "").replace("/", ".")
env_class_name = config["environment"]["class"]

env_module = importlib.import_module(env_file)
env_class = getattr(env_module, env_class_name)
env = env_class()

print("✅ Environment loaded:", env)

tasks_file = config["tasks"]["file"].replace(".py", "").replace("/", ".")
tasks_entry = config["tasks"]["entry"]

tasks_module = importlib.import_module(tasks_file)
tasks_func = getattr(tasks_module, tasks_entry)
tasks = tasks_func()

print("✅ Tasks loaded:", tasks)

grader_file = config["grader"]["file"].replace(".py", "").replace("/", ".")
grader_entry = config["grader"]["entry"]

grader_module = importlib.import_module(grader_file)
grader_func = getattr(grader_module, grader_entry)

print("✅ Grader loaded:", grader_func)

# 🔥 Test step execution
test_patient = {
    "symptoms": "fever",
    "arrival_type": "walk-in",
    "age": 30,
    "duration_hours": 2
}

state = env.reset(test_patient)
action = env.choose_action(state)
result, reward = env.step(test_patient, action)

print("✅ Step working:", result)

print("🎉 VALIDATION PASSED")