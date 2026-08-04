# builder_api.py — Builder-safe module listing with ignore.list
# Peter + Copilot — 2026-08-04

from fastapi import APIRouter
from core.loader import load_ignore_list
import os

router = APIRouter()

MODULES_DIR = "modules"

# ------------------------------------------------------------
# List installed modules (ignore.list aware)
# ------------------------------------------------------------
@router.get("/builder/modules")
def builder_modules():
    ignore = load_ignore_list()
    modules = []

    if not os.path.isdir(MODULES_DIR):
        return modules

    for name in os.listdir(MODULES_DIR):
        if name in ignore:
            continue

        path = f"{MODULES_DIR}/{name}"
        if os.path.isdir(path):
            modules.append(name)

    return modules
