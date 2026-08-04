# toggles.py — FINAL FIXED VERSION (Default OFF + Script Execution + ignore.list + NAV REGEN)
# Peter + Copilot — 2026-08-04

import json
import os
from fastapi import APIRouter, HTTPException
from core.loader import load_ignore_list
from ui.frontend.navigation import refresh_navigation   # ⭐ ADDED: nav regeneration

router = APIRouter()

TOGGLE_FILE = "config/toggles.json"
MODULES_DIR = "modules"

# -------------------------------------------------------------
# Load toggles.json
# -------------------------------------------------------------
def load_toggles():
    """Load toggles.json. Missing entries default to OFF."""
    if not os.path.isfile(TOGGLE_FILE):
        return {}

    try:
        with open(TOGGLE_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

# -------------------------------------------------------------
# Save toggles.json
# -------------------------------------------------------------
def save_toggles(data):
    """Write toggles.json safely."""
    try:
        with open(TOGGLE_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------------------
# Run install.sh or uninstall.sh
# -------------------------------------------------------------
def run_script(module, script_name):
    script_path = os.path.join(MODULES_DIR, module, script_name)
    if not os.path.exists(script_path):
        return f"{script_name} missing"

    # Ensure executable
    try:
        os.chmod(script_path, 0o755)
    except:
        return f"chmod failed for {script_name}"

    result = os.system(script_path)
    return "ok" if result == 0 else f"{script_name} failed"

# -------------------------------------------------------------
# GET /toggles/get
# -------------------------------------------------------------
@router.get("/toggles/get")
def get_toggles():
    """Return all toggle states, filtered by ignore.list."""
    toggles = load_toggles()
    ignore = load_ignore_list()

    # Drop any ignored keys like _meta
    filtered = {k: v for k, v in toggles.items() if k not in ignore}
    return filtered

# -------------------------------------------------------------
# POST /toggles/set
# Body:
# {
#   "name": "example",
#   "state": true/false
# }
# -------------------------------------------------------------
@router.post("/toggles/set")
def set_toggle(payload: dict):
    name = payload.get("name")
    state = payload.get("state")

    if name is None or state is None:
        raise HTTPException(status_code=400, detail="Missing name/state")

    # Respect ignore.list: do not allow toggling ignored entries
    ignore = load_ignore_list()
    if name in ignore:
        raise HTTPException(status_code=400, detail="Toggle is ignored")

    toggles = load_toggles()
    toggles[name] = bool(state)
    save_toggles(toggles)

    # Run install/uninstall scripts
    if state:
        result = run_script(name, "install.sh")
    else:
        result = run_script(name, "uninstall.sh")

    if result != "ok":
        return {"error": result}

    # ⭐ CRITICAL FIX: regenerate nav EVERY time a toggle changes
    refresh_navigation()

    return {"ok": True, "name": name, "state": state}
