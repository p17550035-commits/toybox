# logger.py — FULL REPLACEMENT (with verbose support)
# Updated: 2026-08-04 @ 04:15 EDT
# Author: Copilot + Peter
# Purpose: Unified logging system for ToyBox (main + verbose)
# Notes:
#   - Ensures logs/ directory exists
#   - Main log: toybox.log (clean)
#   - Verbose log: verbose.log (debug)
#   - Used by builder.py, navigation.py, lifecycle.py, toggles.py

import os
import datetime

LOG_DIR = "logs"
LOG_FILE = f"{LOG_DIR}/toybox.log"
VERBOSE_LOG_FILE = f"{LOG_DIR}/verbose.log"

# Ensure logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)


# ------------------------------------------------------------
# Main Log (clean)
# ------------------------------------------------------------

def log(msg):
    """Write a timestamped log entry to the main log."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"

    with open(LOG_FILE, "a") as f:
        f.write(entry)

    print(f"[ToyBox] {msg}")


def read_logs():
    """Return full main log text."""
    if not os.path.exists(LOG_FILE):
        return ""
    with open(LOG_FILE, "r") as f:
        return f.read()


# ------------------------------------------------------------
# Verbose Log (debug)
# ------------------------------------------------------------

def log_verbose(msg):
    """Write a timestamped entry to verbose.log (debug only)."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {msg}\n"

    with open(VERBOSE_LOG_FILE, "a") as f:
        f.write(entry)

    # Do NOT print verbose logs to console
    # They are meant for debug tab only.


def read_verbose_logs():
    """Return full verbose log text."""
    if not os.path.exists(VERBOSE_LOG_FILE):
        return ""
    with open(VERBOSE_LOG_FILE, "r") as f:
        return f.read()
