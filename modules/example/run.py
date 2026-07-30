from core.registry import register

def execute():
    return "Example module executed!"

register("example", execute)
