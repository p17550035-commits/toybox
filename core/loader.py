import pkgutil
import importlib
import modules
from core.toggles import is_enabled

def load_modules():
    loaded = {}
    for finder, name, ispkg in pkgutil.iter_modules(modules.__path__):
        if not is_enabled(name):
            continue
        try:
            mod = importlib.import_module(f"modules.{name}.run")
            loaded[name] = mod
        except Exception as e:
            print(f"Failed to load module {name}: {e}")
    return loaded
