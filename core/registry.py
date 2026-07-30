registry = {}

def register(name, func):
    registry[name] = func

def get(name):
    return registry.get(name)
