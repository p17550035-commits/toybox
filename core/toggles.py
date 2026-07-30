import json
import os

TOGGLE_FILE = "config/toggles.json"

def load_toggles():
    if not os.path.exists(TOGGLE_FILE):
        return {}
    with open(TOGGLE_FILE, "r") as f:
        return json.load(f)

def save_toggles(toggles):
    with open(TOGGLE_FILE, "w") as f:
        json.dump(toggles, f, indent=2)

def is_enabled(name):
    toggles = load_toggles()
    return toggles.get(name, True)

def set_toggle(name, value=True):
    toggles = load_toggles()
    toggles[name] = value
    save_toggles(toggles)
