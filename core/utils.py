# utils.py — FULL REPLACEMENT
# Updated: 2026-08-04 @ 03:55 EDT
# Author: Copilot + Peter
# Purpose: Thin wrapper around core.logger.log
# Notes:
#   - Prevents duplicate logging systems
#   - Ensures all logs go through unified logger

from core.logger import log as core_log

def log(msg):
    """Forward all utility logs to the main logger."""
    core_log(msg)
