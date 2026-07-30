import subprocess
import shutil
import os
from core.logger import log
from core.registry import registry, register
from core.toggles import set_toggle, load_toggles, save_toggles
from ui.navigation import refresh_navigation   # ← ADDED

def activate_module(name):
    log(f"Activating module: {name}")

    install_script = f"modules/{name}/install.sh"
    if os.path.exists(install_script):
        try:
            subprocess.call(["bash", install_script])
        except Exception as e:
            log(f"Install script failed for {name}: {e}")

    set_toggle(name, True)
    register(name, None)

    refresh_navigation()   # ← ADDED
    log(f"Module {name} activated + registered.")

def deactivate_module(name):
    log(f"Deactivating module: {name}")

    uninstall_script = f"modules/{name}/uninstall.sh"
    if os.path.exists(uninstall_script):
        try:
            subprocess.call(["bash", uninstall_script])
        except Exception as e:
            log(f"Uninstall script failed for {name}: {e}")

    set_toggle(name, False)
    registry.pop(name, None)

    refresh_navigation()   # ← ADDED
    log(f"Module {name} deactivated + unregistered.")

def delete_module(name):
    log(f"Deleting module: {name}")

    # Deactivate first
    deactivate_module(name)

    # Remove toggle entry
    toggles = load_toggles()
    if name in toggles:
        del toggles[name]
        save_toggles(toggles)

    # Delete module folder (removes UI files too)
    module_path = f"modules/{name}"
    if os.path.exists(module_path):
        shutil.rmtree(module_path)

    refresh_navigation()   # ← ADDED
    log(f"Module {name} deleted successfully.")
