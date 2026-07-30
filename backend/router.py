from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from ui.page_loader import load_builtin_page, load_module_page
from ui.builder import builder_create_from_json, builder_delete_from_json
from core.toggles import set_toggle, load_toggles
from core.lifecycle import activate_module, deactivate_module

router = APIRouter()

# ---------------------------
# Built-in UI pages
# ---------------------------
@router.get("/ui/{page}", response_class=HTMLResponse)
def serve_builtin_page(page: str):
    return load_builtin_page(page)

# ---------------------------
# Module UI pages
# ---------------------------
@router.get("/modules/{name}", response_class=HTMLResponse)
def serve_module_page(name: str):
    return load_module_page(name)

# ---------------------------
# Builder: Create Module
# ---------------------------
@router.post("/builder/create")
async def builder_create(request: Request):
    data = await request.json()
    result = builder_create_from_json(data)
    return JSONResponse({"status": "ok", "message": f"Module '{data.get('name')}' created."})

# ---------------------------
# Builder: Delete Module
# ---------------------------
@router.post("/builder/delete")
async def builder_delete(request: Request):
    data = await request.json()
    name = data.get("name")
    builder_delete_from_json(name)
    return JSONResponse({"status": "ok", "message": f"Module '{name}' deleted."})

# ---------------------------
# Builder: List Modules
# ---------------------------
@router.get("/builder/list")
def builder_list():
    toggles = load_toggles()
    return JSONResponse({"modules": list(toggles.keys())})

# ---------------------------
# Tools: Toggle ON/OFF
# ---------------------------
@router.post("/tools/toggle")
async def toggle_module(request: Request):
    data = await request.json()
    name = data.get("name")
    state = data.get("state")

    if state:
        activate_module(name)
    else:
        deactivate_module(name)

    return JSONResponse({"status": "ok", "module": name, "state": state})
