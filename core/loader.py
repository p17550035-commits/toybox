import pkgutil
import importlib
import modules

def load_modules():
    loaded = {}
    for finder, name, ispkg in pkgutil.iter_modules(modules.__path__):
        mod = importlib.import_module(f"modules.{name}.run")
        loaded[name] = mod
    return loaded
