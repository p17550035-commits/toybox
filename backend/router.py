# router.py — CLEAN FOLDER-BASED ROUTER (FIXED)
# Built-in pages use explicit routes
# Modules use dynamic routing only

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse

from ui.builder import builder_create_from_json, builder_delete_from_json
from core.toggles import load_toggles, set_toggle
from core.lifecycle import activate_module, deactivate_module
from core.logger import read_logs, read_verbose_logs
from core.settings import load_settings, save_settings, DEFAULT_SETTINGS

import importlib.util

router = APIRouter()

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

def sanitize_name(name: str) -> str:
    safe = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
    return safe.lower()

# ------------------------------------------------------------
# BUILT-IN UI PAGES (EXPLICIT ROUTES)
# ------------------------------------------------------------

@router.get("/ui/tools", response_class=FileResponse)
def ui_tools():
    return FileResponse("ui/tools/tools.html")

@router.get("/ui/builder", response_class=FileResponse)
def ui_builder():
    return FileResponse("ui/builder/builder.html")

@router.get("/ui/dashboard", response_class=FileResponse)
def ui_dashboard():
    return FileResponse("ui/dashboard/dashboard.html")

@router.get("/ui/settings", response_class=FileResponse)
def ui_settings():
    return FileResponse("ui/settings/settings.html")

@router.get("/ui/logs", response_class=FileResponse)
def ui_logs():
    return FileResponse("ui/logs/logs.html")

# ------------------------------------------------------------
# MODULE UI PAGES (DYNAMIC)
# ------------------------------------------------------------

@router.get("/modules/{name}", response_class=FileResponse)
def serve_module_page(name: str):
    name = sanitize_name(name)
    return FileResponse(f"modules/{name}/{name}.html")

# ------------------------------------------------------------
# MODULE RUN ENDPOINT (DYNAMIC)
# ------------------------------------------------------------

@router.get("/modules/{name}/run")
def module_run(name: str):
    name = sanitize_name(name)
    module_path = f"modules/{name}/run.py"

    spec = importlib.util.spec_from_file_location(f"{name}_run", module_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    return mod.run()

# ------------------------------------------------------------
# BUILDER: CREATE MODULE (JSON VERSION — FIXED)
# ------------------------------------------------------------

@router.post("/builder/create")
async def builder_create(request: Request):
    data = await request.json()
    builder_create_from_json(data)
    return JSONResponse({"status": "ok", "message": f"Module '{data.get('name')}' created."})

# ------------------------------------------------------------
# BUILDER: DELETE MODULE
# ------------------------------------------------------------

@router.post("/builder/delete")
async def builder_delete(request: Request):
    data = await request.json()
    name = sanitize_name(data.get("name"))
    builder_delete_from_json(name)
    return JSONResponse({"status": "ok", "message": f"Module '{name}' deleted."})

# ------------------------------------------------------------
# BUILDER: LIST MODULES
# ------------------------------------------------------------

@router.get("/builder/list")
def builder_list():
    toggles = load_toggles()
    return JSONResponse({"modules": list(toggles.keys())})

# ------------------------------------------------------------
# TOOLS: TOGGLE ON/OFF
# ------------------------------------------------------------

@router.post("/tools/toggle")
async def toggle_module(request: Request):
    data = await request.json()
    return set_toggle(data)

# ------------------------------------------------------------
# LOGS (MAIN)
# ------------------------------------------------------------

@router.get("/logs")
def get_logs():
    return HTMLResponse(read_logs())

# ------------------------------------------------------------
# VERBOSE LOGS (DEBUG)
# ------------------------------------------------------------

@router.get("/verbose_logs")
def get_verbose_logs():
    return HTMLResponse(read_verbose_logs())

# ------------------------------------------------------------
# SETTINGS: GET
# ------------------------------------------------------------

@router.get("/settings/get")
def settings_get():
    settings = load_settings()
    return JSONResponse({"settings": settings})

# ------------------------------------------------------------
# SETTINGS: SAVE
# ------------------------------------------------------------

@router.post("/settings/save")
async def settings_save(request: Request):
    data = await request.json()
    try:
        save_settings(data)
        return JSONResponse({"status": "ok", "message": "Settings saved."})
    except Exception as e:
        return JSONResponse({"error": f"Failed to save settings: {e}"})

# ------------------------------------------------------------
# SETTINGS: RESET
# ------------------------------------------------------------

@router.post("/settings/reset")
def settings_reset():
    try:
        save_settings(DEFAULT_SETTINGS)
        return JSONResponse({"status": "ok", "message": "Settings reset to defaults."})
    except Exception as e:
        return JSONResponse({"error": f"Failed to reset settings: {e}"})
