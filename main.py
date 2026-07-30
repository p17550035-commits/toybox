from core.loader import load_modules
from ui.cli import start_cli

def main():
    modules = load_modules()
    start_cli(modules)

if __name__ == "__main__":
    main()
