from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

from core.loader import load_modules
from ui.cli import start_cli
from core.logger import log

# Import router (all wiring lives there)
from backend.router import router

app = FastAPI()

# STATIC FILE MOUNTS (required for UI)
app.mount("/ui", StaticFiles(directory="ui"), name="ui")
app.mount("/modules", StaticFiles(directory="modules"), name="modules")

# ROUTER
app.include_router(router)

def main():
    log("Starting ToyBox...")

    # Load modules for CLI mode
    modules = load_modules()
    log(f"Loaded modules: {list(modules.keys())}")

    # Start CLI
    start_cli(modules)

    # Start FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
