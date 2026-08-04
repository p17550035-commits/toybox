# page_loader.py — NAV ONLY injection (static‑safe)
# Updated: 2026-08-04 @ 11:20 EDT
# Author: Copilot + Peter
# Purpose: Inject ONLY the navigation bar into built‑in + module pages
# Notes:
#   - NO global CSS
#   - NO global JS
#   - NO page-specific CSS/JS injection
#   - NO module CSS/JS injection
#   - Built‑ins remain fully static
#   - Modules remain dynamic
#   - Tools.js remains untouched

import os
from ui.frontend.navigation import refresh_navigation

NAV_FILE = "ui/frontend/generated_nav.html"

# ---------------------------------------------------------
# Inject navigation HTML into <div id="nav"></div>
# ---------------------------------------------------------
def inject_navigation(html: str) -> str:
    # Always regenerate nav before injecting
    refresh_navigation()

    if not os.path.exists(NAV_FILE):
        return html

    with open(NAV_FILE, "r") as f:
        nav_html = f.read()

    return html.replace('<div id="nav"></div>', nav_html)

# ---------------------------------------------------------
# Load any page and apply ONLY nav injection
# ---------------------------------------------------------
def load_page(path: str, page_name=None, module_name=None):
    if not os.path.exists(path):
        return f"<h1>404 - Page Not Found</h1><p>{path} does not exist.</p>"

    with open(path, "r") as f:
        html = f.read()

    # Inject ONLY nav — no CSS/JS injection
    html = inject_navigation(html)
    return html

# ---------------------------------------------------------
# Built-in pages (static folder structure)
# ---------------------------------------------------------
def load_builtin_page(name: str):
    path = f"ui/{name}/{name}.html"
    return load_page(path, page_name=name)

# ---------------------------------------------------------
# Module pages (dynamic)
# ---------------------------------------------------------
def load_module_page(module_name: str):
    module_name = "".join(c for c in module_name if c.isalnum() or c in ("_", "-")).lower()
    path = f"modules/{module_name}/{module_name}.html"
    return load_page(path, module_name=module_name)
