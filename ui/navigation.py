import os
from core.toggles import load_toggles

# Built-in pages (always visible)
BUILTIN_PAGES = [
    ("Dashboard", "dashboard.html"),
    ("Tools", "tools.html"),
    ("Logs", "logs.html"),
    ("Settings", "settings.html")
]

NAV_PATH = "ui/generated_nav.html"

def build_navigation():
    """
    Builds the Fluent-style navigation bar based on active modules.
    Writes the final HTML to ui/generated_nav.html.
    """

    toggles = load_toggles()

    # Start building HTML
    html = []
    html.append("<div class='nav-bar'>")

    # Built-in pages first
    for label, file in BUILTIN_PAGES:
        html.append(f"<a class='nav-tab' href='/{file}'>{label}</a>")

    # Active modules (toggled ON)
    for module_name, state in toggles.items():
        if state:  # Only show active modules
            html.append(
                f"<a class='nav-tab' href='/modules/{module_name}/page.html'>{module_name}</a>"
            )

    html.append("</div>")

    # Write final nav file
    with open(NAV_PATH, "w") as f:
        f.write("\n".join(html))


def refresh_navigation():
    """
    Rebuilds the navigation bar whenever modules are toggled ON/OFF or deleted.
    """
    build_navigation()


# CSS for Fluent tabs (auto-wrap)
NAV_CSS = """
.nav-bar {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    background: #f0f0f0;
    padding: 10px;
    border-bottom: 1px solid #ccc;
}

.nav-tab {
    padding: 8px 14px;
    background: #ffffff;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    text-decoration: none;
    color: #333;
    font-family: sans-serif;
    transition: background 0.2s;
}

.nav-tab:hover {
    background: #e6e6e6;
}
"""

# Write CSS file once
NAV_CSS_PATH = "ui/navigation.css"
if not os.path.exists(NAV_CSS_PATH):
    with open(NAV_CSS_PATH, "w") as f:
        f.write(NAV_CSS)

# Build initial nav on first import
build_navigation()
