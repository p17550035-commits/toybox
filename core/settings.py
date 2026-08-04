# settings.py — FULL FILE
# Updated: 2026-08-04 @ 04:55 EDT
# Author: Copilot + Peter
# Purpose: Global backend settings for ToyBox
# Notes:
#   - Provides a single backend home for all global settings
#   - Loads config/settings.json safely
#   - Supports future UI-driven settings
#   - Used by lifecycle.py, logger.py, router.py, etc.

import os
import json
from core.logger import log

SETTINGS_DIR = "config"
SETTINGS_FILE = f"{SETTINGS_DIR}/settings.json"

# Ensure directory exists
os.makedirs(SETTINGS_DIR, exist_ok=True)

# Default settings
DEFAULT_SETTINGS = {
    "verbose_logging": False,
    "ui_theme": "dark",
    "safe_mode": False,
    "version": "1.0.0"
}


def load_settings():
    """Load settings.json safely. Returns defaults if missing/invalid."""
    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS

    try:
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
        return {**DEFAULT_SETTINGS, **data}  # merge defaults + overrides
    except Exception as e:
        log(f"Failed to load settings.json: {e}. Using defaults.")
        return DEFAULT_SETTINGS


def save_settings(data):
    """Write settings.json safely."""
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        log(f"Failed to save settings.json: {e}")


def get(key):
    """Retrieve a single setting."""
    settings = load_settings()
    return settings.get(key, DEFAULT_SETTINGS.get(key))


def set(key, value):
    """Update a single setting."""
    settings = load_settings()
    settings[key] = value
    save_settings(settings)
    log(f"Setting updated: {key} → {value}")


# Exported global flags
VERBOSE_LOGGING = get("verbose_logging")
