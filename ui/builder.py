import os
import json
from json import JSONDecodeError

from core.logger import log
from core.toggles import load_toggles, save_toggles
from core.lifecycle import delete_module
from ui.frontend.navigation import refresh_navigation

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def sanitize_name(name: str) -> str:
    safe = "".join(c for c in name if c.isalnum() or c in ("_", "-"))
    return safe.lower()


def write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def default_config():
    return {
        "template": "fluent",

        "html_override": "",
        "css_override": "",
        "js_override": "",

        "inject": {
            "html": True,
            "css": True,
            "js": True,
        },

        "cards": {
            "count": 5,
            "names": ["Info", "Controls", "Output", "Logs", "Extra"],
        },

        "metadata": {
            "author": "ToyBox Builder",
            "version": "1.0.0",
            "tags": [],
        },
    }


def validate_config(config_raw: str):
    warnings = []

    if not config_raw.strip():
        return default_config(), warnings

    try:
        cfg = json.loads(config_raw)
        # Merge with defaults so missing keys don’t break things
        base = default_config()
        for k, v in base.items():
            if k not in cfg:
                cfg[k] = v
        # Deep merge for inject/cards/metadata
        for key in ("inject", "cards", "metadata"):
            if key in base:
                if key not in cfg or not isinstance(cfg[key], dict):
                    cfg[key] = base[key]
                else:
                    for sub_k, sub_v in base[key].items():
                        if sub_k not in cfg[key]:
                            cfg[key][sub_k] = sub_v
        return cfg, warnings
    except JSONDecodeError as e:
        warning = {
            "line": e.lineno,
            "column": e.colno,
            "message": e.msg,
        }
        warnings.append(warning)

        log(
            f"CONFIG JSON ERROR: line {e.lineno}, column {e.colno} — {e.msg}. "
            f"Falling back to default config for this module."
        )

        return default_config(), warnings


# ------------------------------------------------------------
# Core module creation logic
# ------------------------------------------------------------
def _create_module_internal(
    name,
    description,
    category,
    page_type,
    code,
    install_script,
    uninstall_script,
    config_raw,
    source_label="UI",
):
    name = sanitize_name(name.strip())
    if not name:
        return {"error": "Module name required"}, []

    config_data, config_warnings = validate_config(config_raw)

    template_mode = config_data.get("template", "fluent")
    inject_cfg = config_data.get("inject", {})
    inject_html = bool(inject_cfg.get("html", True))
    inject_css = bool(inject_cfg.get("css", True))
    inject_js = bool(inject_cfg.get("js", True))

    cards_cfg = config_data.get("cards", {})
    cards_count = int(cards_cfg.get("count", 5))
    if cards_count < 0:
        cards_count = 0
    card_names = cards_cfg.get("names", [])
    if not isinstance(card_names, list):
        card_names = []

    metadata_cfg = config_data.get("metadata", {})

    module_path = f"modules/{name}"
    os.makedirs(module_path, exist_ok=True)

    # Write scripts
    with open(f"{module_path}/run.py", "w") as f:
        f.write(code)

    with open(f"{module_path}/install.sh", "w") as f:
        f.write(install_script)
    os.chmod(f"{module_path}/install.sh", 0o755)

    with open(f"{module_path}/uninstall.sh", "w") as f:
        f.write(uninstall_script)
    os.chmod(f"{module_path}/uninstall.sh", 0o755)

    # Write config.json (advanced template)
    write_json(f"{module_path}/config.json", config_data)

    # Write metadata.json (merge base + config metadata)
    metadata = {
        "name": name,
        "description": description,
        "category": category,
        "page_type": page_type,
    }
    if isinstance(metadata_cfg, dict):
        for k, v in metadata_cfg.items():
            metadata[k] = v
    write_json(f"{module_path}/metadata.json", metadata)

    # --------------------------------------------------------
    # HTML Template (Dashboard-style Fluent, nav-aware)
    # --------------------------------------------------------
    html_override = config_data.get("html_override", "")
    if template_mode == "none":
        html_template = ""
    elif html_override:
        html_template = html_override
    else:
        # Build card grid
        card_divs = []
        for i in range(cards_count):
            card_id = f"card-{i+1}"
            title = card_names[i] if i < len(card_names) else f"Card {i+1}"
            card_divs.append(
                f"""
        <div class="module-card" id="{card_id}">
            <h2 class="module-card-title">{title}</h2>
            <div class="module-card-body" id="{card_id}-body"></div>
        </div>
                """.rstrip()
            )
        cards_html = "\n".join(card_divs)

        html_template = f"""<!DOCTYPE html>
<html>
<head>
    <title>{name} Module</title>
    <link rel="stylesheet" href="{name}.css">
</head>
<body>

<div id="nav"></div>
<script>
async function injectNav() {{
    try {{
        const res = await fetch("/ui/frontend/generated_nav.html?cache=" + Date.now());
        const html = await res.text();
        document.getElementById("nav").innerHTML = html;
    }} catch (e) {{
        document.getElementById("nav").innerHTML =
            "<div style='padding:10px;background:#300;color:#f88;border-bottom:1px solid #600;'>Navigation failed to load</div>";
    }}
}}
injectNav();
</script>

<h1 class="module-title">{name}</h1>
<p class="module-description">{description}</p>

<div class="module-grid">
{cards_html}
</div>

<script src="{name}.js"></script>
</body>
</html>
"""

    if inject_html and html_template:
        with open(f"{module_path}/{name}.html", "w") as f:
            f.write(html_template)

    # --------------------------------------------------------
    # CSS Template (Fluent dark dashboard-style)
    # --------------------------------------------------------
    css_override = config_data.get("css_override", "")
    if template_mode == "none":
        css_template = ""
    elif css_override:
        css_template = css_override
    else:
        css_template = """
body {
    font-family: system-ui, sans-serif;
    background: #111;
    color: #eee;
    margin: 0;
    padding: 16px;
}

.module-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 10px;
    color: #fafafa;
}

.module-description {
    font-size: 16px;
    color: #bbb;
    margin-bottom: 20px;
}

.module-grid {
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.module-card {
    background: #1b1b1b;
    border: 1px solid #333;
    border-radius: 12px;
    padding: 20px;
}

.module-card-title {
    margin-top: 0;
    margin-bottom: 10px;
    color: #fafafa;
    font-size: 20px;
    font-weight: 600;
}

.module-card-body {
    font-size: 15px;
    color: #ddd;
}

/* Auto-hide empty cards (JS will add .empty) */
.module-card.empty {
    display: none;
}

@media (min-width: 800px) {
    body {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .module-grid {
        width: 800px;
    }
}
""".lstrip()

    if inject_css and css_template:
        with open(f"{module_path}/{name}.css", "w") as f:
            f.write(css_template)

    # --------------------------------------------------------
    # JS Template (wired to /modules/{name}/run)
    # --------------------------------------------------------
    js_override = config_data.get("js_override", "")
    if template_mode == "none":
        js_template = ""
    elif js_override:
        js_template = js_override
    else:
        js_template = f"""
document.addEventListener("DOMContentLoaded", async () => {{
    try {{
        const res = await fetch("/modules/{name}/run");
        const data = await res.json();

        // Expect optional card content in data.cards[0..N]
        if (data.cards && Array.isArray(data.cards)) {{
            data.cards.forEach((card, idx) => {{
                const cardId = "card-" + (idx + 1);
                const cardEl = document.getElementById(cardId);
                const bodyEl = document.getElementById(cardId + "-body");

                if (!cardEl || !bodyEl) return;

                if (card && card.content) {{
                    bodyEl.textContent = card.content;
                    cardEl.classList.remove("empty");
                }} else {{
                    cardEl.classList.add("empty");
                }}
            }});
        }} else {{
            // Fallback: put JSON into first card
            const cardEl = document.getElementById("card-1");
            const bodyEl = document.getElementById("card-1-body");
            if (cardEl && bodyEl) {{
                bodyEl.textContent = JSON.stringify(data, null, 2);
                cardEl.classList.remove("empty");
            }}
        }}
    }} catch (err) {{
        console.error("Failed to load module data:", err);
        const cardEl = document.getElementById("card-1");
        const bodyEl = document.getElementById("card-1-body");
        if (cardEl && bodyEl) {{
            bodyEl.textContent = "Error loading module data: " + err;
            cardEl.classList.remove("empty");
        }}
    }}
}});
""".lstrip()

    if inject_js and js_template:
        with open(f"{module_path}/{name}.js", "w") as f:
            f.write(js_template)

    # --------------------------------------------------------
    # Toggle defaults
    # --------------------------------------------------------
    toggles = load_toggles()
    if name not in toggles:
        toggles[name] = False
    save_toggles(toggles)

    refresh_navigation()

    log(f"Module '{name}' created via {source_label}.")

    if config_warnings:
        for w in config_warnings:
            log(
                f"CONFIG WARNING for module '{name}': "
                f"line {w['line']}, column {w['column']} — {w['message']}"
            )

    response = {
        "status": "ok",
        "name": name,
    }

    if config_warnings:
        response["config_warnings"] = config_warnings

    return response, config_warnings


# ------------------------------------------------------------
# UI JSON Builder Functions
# ------------------------------------------------------------
def builder_create_from_json(data):
    name = data.get("name", "")
    description = data.get("description", "")
    category = data.get("category", "")
    page_type = data.get("page_type", "fluent")
    code = data.get("code", "")
    install_script = data.get("install_script", "")
    uninstall_script = data.get("uninstall_script", "")
    config_data_raw = data.get("config_data", "")

    response, warnings = _create_module_internal(
        name=name,
        description=description,
        category=category,
        page_type=page_type,
        code=code,
        install_script=install_script,
        uninstall_script=uninstall_script,
        config_raw=config_data_raw,
        source_label="UI",
    )

    return response


def builder_delete_from_json(name):
    name = sanitize_name(name)

    if not name:
        return {"error": "Module name required"}

    # --- Respect ignore.list ---
    ignore_path = "ignore.list"
    if os.path.exists(ignore_path):
        with open(ignore_path, "r") as f:
            ignore = [line.strip().lower() for line in f.readlines() if line.strip()]
    else:
        ignore = []

    if name in ignore:
        log(f"DELETE BLOCKED: '{name}' is protected by ignore.list")
        return {
            "status": "ignored",
            "message": f"Module '{name}' is protected by ignore.list",
        }
    # ---------------------------

    delete_module(name)
    refresh_navigation()
    log(f"Module '{name}' deleted via UI.")
    return {"status": "ok", "name": name}


# ------------------------------------------------------------
# CLI Builder (Hidden / Disabled)
# ------------------------------------------------------------
CLI_ENABLED = False  # Flip to True later when you want it active

if CLI_ENABLED:
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

    def builder_cli():
        print("\n=== Module Builder (CLI) ===")
        print("Type 'delete' to open deletion menu.")
        mode = input("Mode (create/delete): ").strip()

        if mode == "delete":
            toggles = load_toggles()
            print("\nModules available for deletion:")
            for name in toggles.keys():
                print(f" - {name}")
            target = input("\nEnter module name to delete: ").strip()
            target = sanitize_name(target)
            if target in toggles:
                delete_module(target)
                refresh_navigation()
                log(f"Module '{target}' deleted via CLI.")
                print(f"\nModule '{target}' deleted successfully.\n")
            else:
                print("\nInvalid module name.\n")
            return

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
        config_data = multiline_input("Enter config data (strict JSON, blank for default):")

        if config_data.strip() == "":
            config_data = ""

        response, warnings = _create_module_internal(
            name=name,
            description=description,
            category=category,
            page_type=page_type,
            code=code,
            install_script=install_script,
            uninstall_script=uninstall_script,
            config_raw=config_data,
            source_label="CLI",
        )

        if "error" in response:
            print(f"\nError: {response['error']}\n")
            return

        print(f"\nModule '{response['name']}' created successfully via CLI.\n")
        if warnings:
            print("Config warnings:")
            for w in warnings:
                print(
                    f" - Line {w['line']}, Column {w['column']}: {w['message']}"
                )
