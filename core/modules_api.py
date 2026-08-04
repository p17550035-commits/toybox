# modules_api.py — Tools-safe module listing with ignore.list (API namespace)
# Peter + Copilot — 2026-08-04

from fastapi import APIRouter
from core.loader import load_ignore_list
import os

router = APIRouter()

MODULES_DIR = "modules"

# ------------------------------------------------------------
# /api/modules/list — used by Tools.js
# ------------------------------------------------------------
@router.get("/api/modules/list")
def modules_list():
    ignore = load_ignore_list()
    modules = []

    if not os.path.isdir(MODULES_DIR):
        return {"modules": modules}

    for name in os.listdir(MODULES_DIR):
        if name in ignore:
            continue

        path = f"{MODULES_DIR}/{name}"
        if os.path.isdir(path):
            modules.append(name)

    return {"modules": modules}
