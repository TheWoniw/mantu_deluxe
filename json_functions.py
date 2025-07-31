import json
import os

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_json(filename, default=None):
    if not os.path.exists(filename):
        return default
    with open(filename, "r") as f:
        return json.load(f)
