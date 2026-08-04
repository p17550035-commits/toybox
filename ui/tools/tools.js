// tools.js — SELF-CONTAINED VERSION (toggle.js merged)
// Updated: 2026-08-04
// Author: Copilot + Peter
// Purpose: Populate toggles + installed modules using backend APIs.

// -------------------------------------------------------------
// INTERNAL: Render toggle list (merged from toggle.js)
// -------------------------------------------------------------
async function renderToggleList(targetId) {
    const box = document.getElementById(targetId);
    if (!box) return;

    try {
        const res = await fetch("/toggles/get");
        const toggles = await res.json();

        box.innerHTML = "";

        Object.keys(toggles).forEach(name => {
            const enabled = toggles[name];

            const row = document.createElement("div");
            row.className = "toggle-row";

            const led = document.createElement("div");
            led.className = "led " + (enabled ? "led-on" : "led-off");

            const label = document.createElement("div");
            label.className = "toggle-label";
            label.textContent = name;

            const btn = document.createElement("button");
            btn.className = "toggle-button";
            btn.textContent = enabled ? "Disable" : "Enable";

            btn.onclick = async () => {
                await fetch("/toggles/set", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        name: name,
                        state: !enabled
                    })
                });

                // Re-render toggles + modules
                await renderToggleList(targetId);
                await loadInstalledModules();

                // ⭐ AUTO-REFRESH NAV BAR (correct path + cache bust) ⭐
                await fetch("/ui/frontend/generated_nav.html?cache=" + Date.now())
                    .then(r => r.text())
                    .then(html => {
                        const nav = document.getElementById("nav");
                        if (nav) nav.innerHTML = html;
                    });
            };

            row.appendChild(led);
            row.appendChild(label);
            row.appendChild(btn);

            box.appendChild(row);
        });

    } catch (err) {
        box.innerHTML = "<div class='module-error'>Failed to load toggles</div>";
        console.error("Toggle list error:", err);
    }
}

// -------------------------------------------------------------
// Load installed modules (backend will filter ignore.list)
// -------------------------------------------------------------
async function loadInstalledModules() {
    const box = document.getElementById("module-list");
    if (!box) return;

    try {
        const res = await fetch("/api/modules/list");
        const json = await res.json();

        box.innerHTML = "";

        json.modules.forEach(name => {
            const div = document.createElement("div");
            div.className = "module-row";
            div.textContent = name;
            box.appendChild(div);
        });

    } catch (err) {
        box.innerHTML = "<div class='module-error'>Failed to load modules</div>";
        console.error("Module list error:", err);
    }
}

// -------------------------------------------------------------
// Load feature toggles
// -------------------------------------------------------------
async function loadToggles() {
    await renderToggleList("toggle-list");
}

// -------------------------------------------------------------
// Initialize Tools page
// -------------------------------------------------------------
async function initTools() {
    await loadInstalledModules();
    await loadToggles();
}

// Run immediately
initTools();
