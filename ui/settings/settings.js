// settings.js — FULL REPLACEMENT
// Updated: 2026-08-04 @ 05:00 EDT
// Author: Copilot + Peter
// Purpose: Dynamic Settings controller for ToyBox
// Notes:
//   - Works with new page_loader.py asset injection.
//   - Loads settings.json from backend (/settings/get).
//   - Saves updated settings back to backend (/settings/save).
//   - Supports text fields, selects, and checkboxes.

// -------------------------------------------------------------
// Load settings.json from backend
// -------------------------------------------------------------
async function loadSettings() {
    try {
        const res = await fetch("/settings/get");
        const json = await res.json();

        if (json.error) {
            showError(json.error);
            return;
        }

        // Fill form fields
        Object.keys(json.settings).forEach(key => {
            const el = document.getElementById(key);
            if (!el) return;

            // Checkbox support
            if (el.type === "checkbox") {
                el.checked = !!json.settings[key];
                return;
            }

            // Text/select fields
            el.value = json.settings[key];
        });

    } catch (err) {
        showError("Failed to load settings: " + err);
    }
}

// -------------------------------------------------------------
// Save updated settings.json to backend
// -------------------------------------------------------------
async function saveSettings() {
    const form = document.getElementById("settings-form");
    if (!form) {
        showError("Settings form missing.");
        return;
    }

    // Collect all form fields into an object
    const data = {};
    const fields = form.querySelectorAll("input, textarea, select");

    fields.forEach(field => {
        // Checkbox support
        if (field.type === "checkbox") {
            data[field.id] = field.checked;
            return;
        }

        // Text/select fields
        data[field.id] = field.value;
    });

    try {
        const res = await fetch("/settings/save", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        const json = await res.json();

        if (json.error) {
            showError(json.error);
            return;
        }

        showSuccess(json.message || "Settings saved.");

    } catch (err) {
        showError("Failed to save settings: " + err);
    }
}

// -------------------------------------------------------------
// Reset settings.json to default values
// -------------------------------------------------------------
async function resetSettings() {
    try {
        const res = await fetch("/settings/reset", {
            method: "POST"
        });

        const json = await res.json();

        if (json.error) {
            showError(json.error);
            return;
        }

        showSuccess(json.message || "Settings reset to defaults.");

        // Reload settings after reset
        loadSettings();

    } catch (err) {
        showError("Reset failed: " + err);
    }
}

// -------------------------------------------------------------
// Auto-load settings when page mounts
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    loadSettings();
});
