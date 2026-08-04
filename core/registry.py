# registry.py — FULL REPLACEMENT
# Updated: 2026-08-04 @ 03:45 EDT
# Author: Copilot + Peter
# Purpose: Simple module registry for ToyBox
# Notes:
#   - Matches builder.py sanitization
#   - Logs registration/unregistration
#   - Safe get() with fallback logging

from core.logger import log


registry = {}


def sanitize_name(name: str) -> str:
    """Match builder.py sanitization rules."""
    safe = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
    return safe.lower()


def register(name: str, func):
    """Register a module's callable or None."""
    name = sanitize_name(name)
    registry[name] = func
    log(f"Registered module: {name}")


def unregister(name: str):
    """Remove a module from the registry."""
    name = sanitize_name(name)
    if name in registry:
        del registry[name]
        log(f"Unregistered module: {name}")
    else:
        log(f"Attempted to unregister missing module: {name}")


def get(name: str):
    """Retrieve a module callable or None."""
    name = sanitize_name(name)
    func = registry.get(name)

    if func is None:
        log(f"Registry lookup: module '{name}' not found.")
    return func
