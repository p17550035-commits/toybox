# navigation.py — FINAL FOLDER-ROUTE VERSION
# Updated: 2026-08-04
# Author: Peter + Copilot
#
# WHY THIS FILE WAS CHANGED:
# ------------------------------------------------------------
# Previously, the navigation generator output links like:
#     /ui/dashboard.html
#     /ui/tools.html
#     /ui/logs.html
#     /ui/settings.html
#     /ui/builder.html
#
# But after the UI restructure, all built‑in pages moved into
# their own folders:
#     ui/dashboard/dashboard.html
#     ui/tools/tools.html
#     ui/logs/logs.html
#     ui/settings/settings.html
#     ui/builder/builder.html
#
# Router.py was updated to serve CLEAN ROUTES:
#     /ui/dashboard  → ui/dashboard/dashboard.html
#     /ui/tools      → ui/tools/tools.html
#     /ui/logs       → ui/logs/logs.html
#     /ui/settings   → ui/settings/settings.html
#     /ui/builder    → ui/builder/builder.html
#
# IMPORTANT:
# The router NO LONGER serves *.html URLs.
# So navigation.py MUST output the CLEAN ROUTES, not the *.html files.
#
# This fix ensures:
#   - No more 404 errors
#   - Nav bar links match router.py exactly
#   - Pretty URLs for the user
#   - Real filesystem paths handled internally by router.py
#
# DO NOT REVERT THIS CHANGE.
# If you output *.html again, the entire UI breaks instantly.
# ------------------------------------------------------------

import os
import json

NAV_FILE = "ui/frontend/generated_nav.html"

def sanitize_name(name: str) -> str:
    safe = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
    return safe.lower()

def load_toggle_states():
    try:
        with open("config/toggles.json", "r") as f:
            return json.load(f)
    except:
        return {}

def generate_navigation():
    tabs = []

    # BUILT-IN TABS — MUST MATCH router.py EXACTLY
    # ------------------------------------------------------------
    # These are the PRETTY ROUTES, not the real file paths.
    # Router.py maps these to the actual HTML files.
    # ------------------------------------------------------------
    builtins = [
        ("Dashboard", "/ui/dashboard"),
        ("Tools", "/ui/tools"),
        ("Logs", "/ui/logs"),
        ("Settings", "/ui/settings"),
        ("Builder", "/ui/builder"),
    ]

    for title, link in builtins:
        tabs.append(f"<a class='nav-tab builtin' href='{link}'>{title}</a>")

    # MODULE TABS — these still use direct HTML files
    # because modules do not have pretty routes.
    toggles = load_toggle_states()

    modules_dir = "modules"
    if os.path.isdir(modules_dir):
        for raw_name in sorted(os.listdir(modules_dir)):
            name = sanitize_name(raw_name)
            module_folder = os.path.join(modules_dir, name)

            if not os.path.isdir(module_folder):
                continue

            html_path = os.path.join(module_folder, f"{name}.html")
            if not os.path.isfile(html_path):
                continue

            if not toggles.get(name, False):
                continue

            title = name
            config_path = os.path.join(module_folder, "config.json")
            if os.path.isfile(config_path):
                try:
                    with open(config_path, "r") as f:
                        config = json.load(f)
                        title = config.get("title", name)
                except:
                    pass

            module_html = f"/modules/{name}/{name}.html"
            tabs.append(
                f"<a class='nav-tab module' href='{module_html}'>{title}</a>"
            )

    html = "<div class='nav-bar'>\n" + "\n".join(tabs) + "\n</div>"
    with open(NAV_FILE, "w") as f:
        f.write(html)

def refresh_navigation():
    generate_navigation()
