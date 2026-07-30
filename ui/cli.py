from ui.tools import tools_ui

def start_cli(modules):
    print("ToyBox CLI ready.")
    print("Loaded modules:", ", ".join(modules.keys()))
    print("\nCommands:")
    print("  tools   - open Tools Page")
    print("  exit    - quit ToyBox")

    while True:
        cmd = input("toybox> ").strip()

        if cmd == "tools":
            tools_ui()
        elif cmd == "exit":
            break
        else:
            print("Unknown command")
