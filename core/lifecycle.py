# lifecycle.py — FULL REPLACEMENT (with verbose support)
# Updated: 2026-08-04 @ 04:10 EDT
# Author: Copilot + Peter
# Purpose: Module activation/deactivation/deletion lifecycle
# Notes:
#   - Matches builder.py sanitization
#   - Loads config.json safely ({} if missing/invalid)
#   - Graceful missing-module handling
#   - Clean logging only
#   - Verbose logging supported but OFF by default

import subprocess
import shutil
import os
import json

from core.logger import log, log_verbose
from core.registry import registry, register
from core.toggles import set_toggle, load_toggles, save_toggles
from ui.frontend.navigation import refresh_navigation
from core.settings import VERBOSE_LOGGING


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def sanitize_name(name: str) -> str:
    """Match builder.py sanitization rules."""
    safe = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
    return safe.lower()


def load_config(name: str):
    """Load config.json safely. Returns {} if missing or invalid."""
    path = f"modules/{name}/config.json"

    if not os.path.exists(path):
        log(f"No config.json found for module '{name}', using defaults.")
        return {}

    try:
        with open(path, "r") as f:
            cfg = json.load(f)
        log(f"Loaded config for module '{name}'.")
        if VERBOSE_LOGGING:
            log_verbose(f"CONFIG for {name}: {json.dumps(cfg, indent=2)}")
        return cfg
    except Exception as e:
        log(f"Config load failed for '{name}': {e}. Using defaults.")
        if VERBOSE_LOGGING:
            log_verbose(f"CONFIG ERROR for {name}: {e}")
        return {}


# ------------------------------------------------------------
# Lifecycle Actions
# ------------------------------------------------------------

def activate_module(name):
    name = sanitize_name(name)
    log(f"Activating module: {name}")

    module_path = f"modules/{name}"
    if not os.path.exists(module_path):
        log(f"Module '{name}' does not exist. Activation aborted.")
        return

    config = load_config(name)

    install_script = f"{module_path}/install.sh"
    if os.path.exists(install_script):
        try:
            subprocess.call(["bash", install_script])
        except Exception as e:
            log(f"Install script failed for {name}: {e}")
            if VERBOSE_LOGGING:
                log_verbose(f"INSTALL ERROR for {name}: {e}")

    set_toggle(name, True)
    register(name, None)

    refresh_navigation()
    log(f"Module {name} activated + registered.")
    if VERBOSE_LOGGING:
        log_verbose(f"ACTIVATE COMPLETE for {name}")


def deactivate_module(name):
    name = sanitize_name(name)
    log(f"Deactivating module: {name}")

    module_path = f"modules/{name}"
    if not os.path.exists(module_path):
        log(f"Module '{name}' does not exist. Deactivation aborted.")
        return

    config = load_config(name)

    uninstall_script = f"{module_path}/uninstall.sh"
    if os.path.exists(uninstall_script):
        try:
            subprocess.call(["bash", uninstall_script])
        except Exception as e:
            log(f"Uninstall script failed for {name}: {e}")
            if VERBOSE_LOGGING:
                log_verbose(f"UNINSTALL ERROR for {name}: {e}")

    set_toggle(name, False)
    registry.pop(name, None)

    refresh_navigation()
    log(f"Module {name} deactivated + unregistered.")
    if VERBOSE_LOGGING:
        log_verbose(f"DEACTIVATE COMPLETE for {name}")


def delete_module(name):
    name = sanitize_name(name)
    log(f"Deleting module: {name}")

    module_path = f"modules/{name}"
    if not os.path.exists(module_path):
        log(f"Module '{name}' does not exist. Delete aborted.")
        return

    # Deactivate first
    deactivate_module(name)

    # Remove toggle entry
    toggles = load_toggles()
    if name in toggles:
        del toggles[name]
        save_toggles(toggles)

    # Delete module folder
    try:
        shutil.rmtree(module_path)
    except Exception as e:
        log(f"Failed to delete module folder '{name}': {e}")
        if VERBOSE_LOGGING:
            log_verbose(f"DELETE ERROR for {name}: {e}")
        return

    refresh_navigation()
    log(f"Module {name} deleted successfully.")
    if VERBOSE_LOGGING:
        log_verbose(f"DELETE COMPLETE for {name}")
