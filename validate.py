import yaml
import importlib

print("🔍 Loading openenv.yaml...")

with open("openenv.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load environment
env_file = config["environment"]["file"].replace(".py", "").replace("/", ".")
env_class_name = config["environment"]["class"]

env_module = importlib.import_module(env_file)
env_class = getattr(env_module, env_class_name)
env = env_class()

print("✅ Environment loaded:", env)

# Load tasks
tasks_file = config["tasks"]["file"].replace(".py", "").replace("/", ".")
tasks_entry = config["tasks"]["entry"]

tasks_module = importlib.import_module(tasks_file)
tasks_func = getattr(tasks_module, tasks_entry)
tasks = tasks_func()

print("✅ Tasks loaded:", tasks)

# Load grader
grader_file = config["grader"]["file"].replace(".py", "").replace("/", ".")
grader_entry = config["grader"]["entry"]

grader_module = importlib.import_module(grader_file)
grader_func = getattr(grader_module, grader_entry)

print("✅ Grader loaded:", grader_func)

print("🎉 VALIDATION PASSED (Structure + imports correct)")