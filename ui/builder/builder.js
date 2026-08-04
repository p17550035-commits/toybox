// builder.js — FULL REPLACEMENT
// Updated: 2026-08-04 @ 00:26 EDT
// Author: Copilot + Peter
// Purpose: Restore dynamic module creation + deletion for ToyBox UI
// Notes:
//   - This version works with the new page_loader.py injection system.
//   - Supports JSON POST (CAT-style backend).
//   - Restores dynamic delete dropdown population.
//   - Restores JS-driven builder logic instead of HTML-only fallback.
//   - All functions are global so builder.html can call them directly.

// -------------------------------------------------------------
// Create Module (JSON POST)
// -------------------------------------------------------------
async function createModule() {
    // Collect form data from builder.html
    const data = {
        name: document.getElementById("name").value.trim(),
        description: document.getElementById("description").value.trim(),
        category: document.getElementById("category").value.trim(),
        page_type: document.getElementById("page_type").value.trim(),
        code: document.getElementById("code").value,
        install_script: document.getElementById("install_script").value,
        uninstall_script: document.getElementById("uninstall_script").value,
        config_data: document.getElementById("config_data").value
    };

    try {
        const res = await fetch("/builder/create", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const json = await res.json();
        alert(json.message || "Module created.");

        // Refresh delete dropdown after creation
        loadModuleList();
    } catch (err) {
        alert("Module creation failed: " + err);
    }
}

// -------------------------------------------------------------
// Delete Module (JSON POST)
// -------------------------------------------------------------
async function deleteModule() {
    const name = document.getElementById("delete_name").value;

    if (!name) {
        alert("Select a module to delete.");
        return;
    }

    try {
        const res = await fetch("/builder/delete", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name })
        });

        const json = await res.json();
        alert(json.message || "Module deleted.");

        // Refresh delete dropdown after deletion
        loadModuleList();
    } catch (err) {
        alert("Module deletion failed: " + err);
    }
}

// -------------------------------------------------------------
// Populate Delete Dropdown
// -------------------------------------------------------------
async function loadModuleList() {
    try {
        const res = await fetch("/builder/list");
        const json = await res.json();

        const select = document.getElementById("delete_name");
        select.innerHTML = "";

        json.modules.forEach(m => {
            const opt = document.createElement("option");
            opt.value = m;
            opt.textContent = m;
            select.appendChild(opt);
        });
    } catch (err) {
        console.error("Failed to load module list:", err);
    }
}

// -------------------------------------------------------------
// Auto-load module list when builder.js is injected
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    loadModuleList();
});
