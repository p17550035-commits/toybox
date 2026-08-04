# page_loader.py — FIXED VERSION (no global CSS/JS)
# Updated: 2026-08-04 @ 06:52 EDT
# Author: Copilot + Peter
# Purpose: UI pipeline (CSS injection + navigation)
# Notes:
#   - NO GLOBAL CSS
#   - NO GLOBAL JS
#   - Built-in pages now live in subfolders (ui/tools/tools.html, etc.)
#   - Module pages unchanged

import os
from ui.frontend.navigation import refresh_navigation

NAV_FILE = "ui/frontend/generated_nav.html"

# ---------------------------------------------------------
# Sanitization (match builder.py + lifecycle.py + toggles.py)
# ---------------------------------------------------------
def sanitize_name(name: str) -> str:
    safe = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
    return safe.lower()

# ---------------------------------------------------------
# Inject navigation HTML into <div id="nav"></div>
# ---------------------------------------------------------
def inject_navigation(html):
    refresh_navigation()

    if not os.path.exists(NAV_FILE):
        return html

    with open(NAV_FILE, "r") as f:
        nav_html = f.read()

    return html.replace('<div id="nav"></div>', nav_html)

# ---------------------------------------------------------
# Inject CSS/JS assets into <head>
# ---------------------------------------------------------
def inject_assets(html, page_name=None, module_name=None):
    css_links = []
    js_links = []

    # Built-in page CSS/JS (new folder structure)
    if page_name:
        page_css = f"ui/{page_name}/{page_name}.css"
        page_js  = f"ui/{page_name}/{page_name}.js"

        if os.path.exists(page_css):
            css_links.append(f'<link rel="stylesheet" href="/{page_css}">')

        if os.path.exists(page_js):
            js_links.append(f'<script src="/{page_js}" defer></script>')

    # Module-specific CSS/JS (unchanged)
    if module_name:
        module_name = sanitize_name(module_name)
        mod_css = f"modules/{module_name}/{module_name}.css"
        mod_js  = f"modules/{module_name}/{module_name}.js"

        if os.path.exists(mod_css):
            css_links.append(f'<link rel="stylesheet" href="/{mod_css}">')

        if os.path.exists(mod_js):
            js_links.append(f'<script src="/{mod_js}" defer></script>')

    # Inject into </head>
    head_injection = "\n".join(css_links + js_links)
    return html.replace("</head>", head_injection + "\n</head>")

# ---------------------------------------------------------
# Load any page and apply navigation + asset injection
# ---------------------------------------------------------
def load_page(path, page_name=None, module_name=None):
    if not os.path.exists(path):
        return f"<h1>404 - Page Not Found</h1><p>{path} does not exist.</p>"

    with open(path, "r") as f:
        html = f.read()

    html = inject_navigation(html)
    html = inject_assets(html, page_name, module_name)
    return html

# ---------------------------------------------------------
# Built-in pages (new folder structure)
# ---------------------------------------------------------
def load_builtin_page(name):
    path = f"ui/{name}/{name}.html"
    return load_page(path, page_name=name)

# ---------------------------------------------------------
# Module pages (unchanged)
# ---------------------------------------------------------
def load_module_page(module_name):
    module_name = sanitize_name(module_name)
    path = f"modules/{module_name}/{module_name}.html"
    return load_page(path, module_name=module_name)
