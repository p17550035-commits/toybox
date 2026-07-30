import os
from core.logger import log
from core.registry import register
from core.toggles import load_toggles, save_toggles
from core.lifecycle import delete_module
from ui.navigation import refresh_navigation

def multiline_input(prompt):
    print(prompt)
    print("(End with a single '.' on a line)")
    lines = []
    while True:
        line = input()
        if line == ".":
            break
        lines.append(line)
    return "\n".join(lines)

def builder_ui():
    print("\n=== Module Builder ===")
    print("Type 'delete' to open deletion menu.")
    mode = input("Mode (create/delete): ").strip()

    if mode == "delete":
        toggles = load_toggles()
        print("\nModules available for deletion:")
        for name in toggles.keys():
            print(f" - {name}")

        target = input("\nEnter module name to delete: ").strip()
        if target in toggles:
            delete_module(target)
            refresh_navigation()
            print(f"\nModule '{target}' deleted successfully.\n")
        else:
            print("\nInvalid module name.\n")
        return

    # CREATE MODE
    name = input("Module Name: ").strip()
    description = multiline_input("Description:")
    category = input("Category: ").strip()

    print("\nPage Type Options:")
    print("  1. Fluent (default)")
    print("  2. Dynamic (advanced)")
    page_type_choice = input("Select page type (1/2): ").strip()
    page_type = "fluent" if page_type_choice != "2" else "dynamic"

    code = multiline_input("Enter module code (run.py):")
    install_script = multiline_input("Enter install script:")
    uninstall_script = multiline_input("Enter uninstall script:")
    config_data = multiline_input("Enter config data (leave blank for {}):")

    if config_data.strip() == "":
        config_data = "{}"

    module_path = f"modules/{name}"
    os.makedirs(module_path, exist_ok=True)

    with open(f"{module_path}/run.py", "w") as f:
        f.write(code)

    with open(f"{module_path}/install.sh", "w") as f:
        f.write(install_script)
    os.chmod(f"{module_path}/install.sh", 0o755)

    with open(f"{module_path}/uninstall.sh", "w") as f:
        f.write(uninstall_script)
    os.chmod(f"{module_path}/uninstall.sh", 0o755)

    with open(f"{module_path}/config.json", "w") as f:
        f.write(config_data)

    metadata = {
        "name": name,
        "description": description,
        "category": category,
        "page_type": page_type
    }
    with open(f"{module_path}/metadata.json", "w") as f:
        f.write(str(metadata))

    if page_type == "fluent":
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="page.css">
</head>
<body>
    <div id="nav"></div>
    <h1>{name} Module</h1>
    <p>{description}</p>
    <script src="page.js"></script>
</body>
</html>
"""
    else:
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="page.css">
</head>
<body>
    <div id="nav"></div>
    <h1>{name} (Dynamic Module)</h1>
    <p>{description}</p>
    <div id="dynamic-content"></div>
    <script src="page.js"></script>
</body>
</html>
"""

    with open(f"{module_path}/page.html", "w") as f:
        f.write(html_template)

    css_template = """
body {
    font-family: sans-serif;
    padding: 20px;
}
"""
    with open(f"{module_path}/page.css", "w") as f:
        f.write(css_template)

    js_template = """
document.addEventListener("DOMContentLoaded", () => {
    console.log("Module page loaded.");
});
"""
    with open(f"{module_path}/page.js", "w") as f:
        f.write(js_template)

    toggles = load_toggles()
    toggles[name] = False
    save_toggles(toggles)

    log(f"Module '{name}' created successfully.")
    print(f"\nModule '{name}' created successfully.")
    print("Tiles cleared. Ready for next module.\n")

# ============================================================
# UI / FastAPI JSON Builder Functions
# ============================================================

def builder_create_from_json(data):
    name = data.get("name", "").strip()
    description = data.get("description", "")
    category = data.get("category", "")
    page_type = data.get("page_type", "fluent")
    code = data.get("code", "")
    install_script = data.get("install_script", "")
    uninstall_script = data.get("uninstall_script", "")
    config_data = data.get("config_data", "{}")

    if not name:
        return {"error": "Module name required"}

    module_path = f"modules/{name}"
    os.makedirs(module_path, exist_ok=True)

    with open(f"{module_path}/run.py", "w") as f:
        f.write(code)

    with open(f"{module_path}/install.sh", "w") as f:
        f.write(install_script)
    os.chmod(f"{module_path}/install.sh", 0o755)

    with open(f"{module_path}/uninstall.sh", "w") as f:
        f.write(uninstall_script)
    os.chmod(f"{module_path}/uninstall.sh", 0o755)

    with open(f"{module_path}/config.json", "w") as f:
        f.write(config_data)

    metadata = {
        "name": name,
        "description": description,
        "category": category,
        "page_type": page_type
    }
    with open(f"{module_path}/metadata.json", "w") as f:
        f.write(str(metadata))

    if page_type == "fluent":
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="page.css">
</head>
<body>
    <div id="nav"></div>
    <h1>{name} Module</h1>
    <p>{description}</p>
    <script src="page.js"></script>
</body>
</html>
"""
    else:
        html_template = f"""
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="page.css">
</head>
<body>
    <div id="nav"></div>
    <h1>{name} (Dynamic Module)</h1>
    <p>{description}</p>
    <div id="dynamic-content"></div>
    <script src="page.js"></script>
</body>
</html>
"""

    with open(f"{module_path}/page.html", "w") as f:
        f.write(html_template)

    css_template = """
body {
    font-family: sans-serif;
    padding: 20px;
}
"""
    with open(f"{module_path}/page.css", "w") as f:
        f.write(css_template)

    js_template = """
document.addEventListener("DOMContentLoaded", () => {
    console.log("Module page loaded.");
});
"""
    with open(f"{module_path}/page.js", "w") as f:
        f.write(js_template)

    toggles = load_toggles()
    toggles[name] = False
    save_toggles(toggles)

    log(f"Module '{name}' created via UI.")
    return {"status": "ok", "name": name}

def builder_delete_from_json(name):
    if not name:
        return {"error": "Module name required"}

    delete_module(name)
    refresh_navigation()

    log(f"Module '{name}' deleted via UI.")
    return {"status": "ok", "name": name}

