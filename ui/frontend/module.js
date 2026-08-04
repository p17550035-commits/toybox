// module.js — FULL REPLACEMENT
// Updated: 2026-08-04 @ 00:59 EDT
// Author: Copilot + Peter
// Purpose: Controller for individual module UI pages
// Notes:
//   - Works with new page_loader.py asset injection.
//   - Handles run/install/uninstall actions for modules.
//   - Loads module metadata + output.
//   - Provides clean API for module-specific UI.

// -------------------------------------------------------------
// Load module metadata (description, category, enabled state)
// -------------------------------------------------------------
async function loadModuleInfo(moduleName) {
    try {
        const res = await fetch(`/modules/info/${moduleName}`);
        const json = await res.json();

        if (json.error) {
            showError(json.error);
            return null;
        }

        return json;

    } catch (err) {
        showError("Failed to load module info: " + err);
        return null;
    }
}

// -------------------------------------------------------------
// Run module (executes run.py)
// -------------------------------------------------------------
async function runModule(moduleName) {
    try {
        const res = await fetch(`/modules/run/${moduleName}`, {
            method: "POST"
        });

        const json = await res.json();

        if (json.error) {
            showError(json.error);
            return;
        }

        showOutput(json.output || "Module executed.");
        showSuccess("Module ran successfully.");

    } catch (err) {
        showError("Module run failed: " + err);
    }
}

// -------------------------------------------------------------
// Install module (executes install.sh)
// -------------------------------------------------------------
async function installModule(moduleName) {
    try {
        const res = await fetch(`/modules/install/${moduleName}`, {
            method: "POST"
        });

        const json = await res.json();

        if (json.error) {
            showError(json.error);
            return;
        }

        showSuccess(json.message || "Module installed.");

    } catch (err) {
        showError("Install failed: " + err);
    }
}

// -------------------------------------------------------------
// Uninstall module (executes uninstall.sh)
// -------------------------------------------------------------
async function uninstallModule(moduleName) {
    try {
        const res = await fetch(`/modules/uninstall/${moduleName}`, {
            method: "POST"
        });

        const json = await res.json();

        if (json.error) {
            showError(json.error);
            return;
        }

        showSuccess(json.message || "Module uninstalled.");

    } catch (err) {
        showError("Uninstall failed: " + err);
    }
}

// -------------------------------------------------------------
// Show output in module page
// -------------------------------------------------------------
function showOutput(text) {
    const box = document.getElementById("module-output");
    if (!box) return;

    box.style.display = "block";
    box.textContent = text;
}

// -------------------------------------------------------------
// Build module action buttons dynamically
// -------------------------------------------------------------
function buildModuleButtons(moduleName) {
    const container = document.getElementById("module-actions");
    if (!container) return;

    container.innerHTML = "";

    const runBtn = document.createElement("button");
    runBtn.className = "tool-button";
    runBtn.textContent = "Run Module";
    runBtn.onclick = () => runModule(moduleName);

    const installBtn = document.createElement("button");
    installBtn.className = "tool-button";
    installBtn.textContent = "Install";
    installBtn.onclick = () => installModule(moduleName);

    const uninstallBtn = document.createElement("button");
    uninstallBtn.className = "tool-button";
    uninstallBtn.textContent = "Uninstall";
    uninstallBtn.onclick = () => uninstallModule(moduleName);

    container.appendChild(runBtn);
    container.appendChild(installBtn);
    container.appendChild(uninstallBtn);
}

// -------------------------------------------------------------
// Auto-load module info when page mounts
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", async () => {
    const moduleName = document.body.getAttribute("data-module");
    if (!moduleName) return;

    const info = await loadModuleInfo(moduleName);
    if (!info) return;

    // Fill description if page has a placeholder
    const desc = document.getElementById("module-description");
    if (desc) desc.textContent = info.description || "No description.";

    // Build action buttons
    buildModuleButtons(moduleName);
});
