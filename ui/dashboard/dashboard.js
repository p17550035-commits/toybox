// dashboard.js — FULL REPLACEMENT (WITH STATUS TICKER)
// Updated: 2026-08-04 @ 16:55 EDT
// Author: Copilot + Peter

// -------------------------------------------------------------
// Load module status (enabled/disabled)
// -------------------------------------------------------------
async function loadModuleStatus() {
    try {
        const res = await fetch("/builder/list");
        const json = await res.json();

        const container = document.getElementById("module-status-list");
        container.innerHTML = "";

        json.modules.forEach(name => {
            const item = document.createElement("div");
            item.className = "module-status-item";

            const nameSpan = document.createElement("span");
            nameSpan.className = "module-status-name";
            nameSpan.textContent = name;

            item.appendChild(nameSpan);
            container.appendChild(item);
        });

    } catch (err) {
        console.error("Failed to load module status:", err);
    }
}

// -------------------------------------------------------------
// Load toggle list (delegates to toggle.js)
// -------------------------------------------------------------
async function loadDashboardToggles() {
    const container = document.getElementById("dashboard-toggle-container");
    if (!container) return;

    container.innerHTML = "";
    await renderToggleList("dashboard-toggle-container");
}

// -------------------------------------------------------------
// Load system status ticker (uptime + modules + toggles)
// -------------------------------------------------------------
async function loadSystemStatus() {
    try {
        const res = await fetch("/modules/status/run");
        const json = await res.json();

        document.getElementById("status-uptime").textContent =
            "Uptime: " + json.uptime + "s";

        document.getElementById("status-modules").textContent =
            "Modules: " + json.modules.join(", ");

        document.getElementById("status-toggles").textContent =
            "Toggles: " + JSON.stringify(json.toggles);

    } catch (err) {
        console.error("Failed to load system status:", err);
    }
}

// -------------------------------------------------------------
// Quick Action: Refresh Dashboard
// -------------------------------------------------------------
async function refreshDashboard() {
    await loadModuleStatus();
    await loadDashboardToggles();
    await loadSystemStatus();
}

// -------------------------------------------------------------
// Auto-load dashboard data when page mounts
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", async () => {
    await loadModuleStatus();
    await loadDashboardToggles();
    await loadSystemStatus();

    // Live ticker every second
    setInterval(loadSystemStatus, 1000);
});
