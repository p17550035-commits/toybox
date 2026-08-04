from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from core.loader import load_modules
from core.logger import log

# Routers
from backend.router import router
from core.toggles import router as toggles_router
from core.builder_api import router as builder_router
from core.modules_api import router as modules_router

app = FastAPI()

# ROUTERS
app.include_router(router)
app.include_router(toggles_router)
app.include_router(builder_router)
app.include_router(modules_router)

# ------------------------------------------------------------
# STATIC FILES — FIXED ORDER
# ------------------------------------------------------------

# Serve builder folder FIRST (this is the fix)
app.mount("/ui/builder", StaticFiles(directory="ui/builder"), name="builder")

# Serve other UI folders
app.mount("/ui/frontend", StaticFiles(directory="ui/frontend"), name="frontend")
app.mount("/ui/dashboard", StaticFiles(directory="ui/dashboard"), name="dashboard")
app.mount("/ui/settings", StaticFiles(directory="ui/settings"), name="settings")
app.mount("/ui/logs", StaticFiles(directory="ui/logs"), name="logs")

# Fallback for anything else under /ui
app.mount("/ui", StaticFiles(directory="ui"), name="ui")

# Modules static mount
app.mount("/modules", StaticFiles(directory="modules"), name="modules")

def main():
    log("Starting ToyBox...")

    modules = load_modules()
    log(f"Loaded modules: {list(modules.keys())}")

    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
