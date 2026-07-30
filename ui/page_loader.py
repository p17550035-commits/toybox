import os

NAV_FILE = "ui/generated_nav.html"

def inject_navigation(html):
    """
    Injects the generated navigation bar into any HTML page
    that contains <div id="nav"></div>.
    """
    if not os.path.exists(NAV_FILE):
        return html

    with open(NAV_FILE, "r") as f:
        nav_html = f.read()

    return html.replace("<div id=\"nav\"></div>", nav_html)


def load_page(path):
    """
    Loads an HTML page from disk and injects navigation.
    Returns the final HTML string.
    """
    if not os.path.exists(path):
        return f"<h1>404 - Page Not Found</h1><p>{path} does not exist.</p>"

    with open(path, "r") as f:
        html = f.read()

    return inject_navigation(html)


def load_builtin_page(name):
    """
    Loads a built-in UI page (dashboard, tools, logs, settings).
    """
    path = f"ui/{name}.html"
    return load_page(path)


def load_module_page(module_name):
    """
    Loads a module's page.html from its folder.
    """
    path = f"modules/{module_name}/page.html"
    return load_page(path)
