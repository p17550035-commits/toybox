from core.toggles import load_toggles
from core.lifecycle import activate_module, deactivate_module
from core.registry import register, registry
from ui.navigation import refresh_navigation   # ← ADDED

def led(state):
    return "🟢" if state else "🔴"

def tools_ui():
    while True:
        toggles = load_toggles()

        print("\n=== Tools Page ===")
        for name, state in toggles.items():
            print(f"{led(state)} {name}: {'ON' if state else 'OFF'}")

        print("\nCommands:")
        print("  on <module>    - activate + install + register")
        print("  off <module>   - deactivate + uninstall + unregister")
        print("  builder        - open Module Builder")
        print("  exit")

        cmd = input("tools> ").strip().split()

        if not cmd:
            continue

        if cmd[0] == "exit":
            break

        if cmd[0] == "builder":
            from ui.builder import builder_ui
            builder_ui()
            refresh_navigation()   # ← ADDED
            continue

        if len(cmd) != 2:
            print("Invalid command")
            continue

        action, module = cmd

        if action == "on":
            activate_module(module)
            register(module, None)
            refresh_navigation()   # ← ADDED
            print(f"🟢 {module} activated + registered.")

        elif action == "off":
            deactivate_module(module)
            registry.pop(module, None)
            refresh_navigation()   # ← ADDED
            print(f"🔴 {module} deactivated + unregistered.")

        else:
            print("Unknown action")
