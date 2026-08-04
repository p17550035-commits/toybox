from core.toggles import load_toggles
from core.loader import load_modules
import time

start_time = time.time()

def get_status():
    toggles = load_toggles()
    modules = load_modules()
    uptime = int(time.time() - start_time)

    return {
        "uptime": uptime,
        "modules": list(modules.keys()),
        "toggles": toggles
    }

def run():
    return get_status()