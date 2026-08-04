# loader.py — FINAL VERSION (Loads ONLY toggled ON modules + ignore.list)
# Peter + Copilot — 2026-08-04

import os
import importlib.util
import json
from core.logger import log

MODULES_DIR = "modules"
TOGGLE_FILE = "config/toggles.json"
IGNORE_FILE = "config/ignore.list"

# -------------------------------------------------------------
# Sanitize module name
# -------------------------------------------------------------
def sanitize_name(name: str) -> str:
    safe = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
    return safe.lower()

# -------------------------------------------------------------
# Load ignore.list
# -------------------------------------------------------------
def load_ignore_list():
    if not os.path.isfile(IGNORE_FILE):
        return set()

    try:
        with open(IGNORE_FILE, "r") as f:
            lines = f.read().splitlines()
            return set([x.strip() for x in lines if x.strip()])
    except:
        return set()

# -------------------------------------------------------------
# Load toggle states
# -------------------------------------------------------------
def load_toggle_states():
    """Load toggles.json. Missing entries default to OFF."""
    try:
        with open(TOGGLE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# -------------------------------------------------------------
# Load ONLY modules toggled ON
# -------------------------------------------------------------
def load_modules():
    loaded = {}
    toggles = load_toggle_states()
    ignore = load_ignore_list()

    if not os.path.isdir(MODULES_DIR):
        return loaded

    for raw_name in sorted(os.listdir(MODULES_DIR)):
        name = sanitize_name(raw_name)
        module_folder = os.path.join(MODULES_DIR, name)

        # Skip ignored modules
        if name in ignore:
            log(f"Module '{name}' ignored via ignore.list")
            continue

        # Skip non-directories
        if not os.path.isdir(module_folder):
            continue

        # Skip modules that are OFF
        if not toggles.get(name, False):
            log(f"Module '{name}' is OFF — skipping")
            continue

        run_path = os.path.join(module_folder, "run.py")
        if not os.path.isfile(run_path):
            log(f"Module '{name}' has no run.py — skipping")
            continue

        try:
            spec = importlib.util.spec_from_file_location(name, run_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            loaded[name] = mod
            log(f"Loaded module: {name}")

        except Exception as e:
            log(f"Failed to load module '{name}': {e}")
            continue

    return loaded
