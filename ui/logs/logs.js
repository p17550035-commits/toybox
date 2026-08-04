// logs.js — FULL REPLACEMENT (main + verbose)
// Updated: 2026-08-04 @ 04:20 EDT
// Author: Copilot + Peter
// Purpose: Dual-log viewer (main + verbose)
// Notes:
//   - Main logs from /logs
//   - Verbose logs from /verbose_logs
//   - Tabs handled by logs.html
//   - Filtering only applies to main logs
//   - Verbose logs show raw entries (no filter)

let rawLines = [];        // main log lines
let verboseLines = [];    // verbose log lines
let autoScroll = true;

// -------------------------------------------------------------
// Fetch MAIN logs
// -------------------------------------------------------------
async function loadLogs() {
    try {
        const res = await fetch("/logs");
        const text = await res.text();

        rawLines = text.split("\n").filter(line => line.trim().length > 0);
        applyLogFilter();

    } catch (err) {
        showError("Failed to load logs: " + err);
    }
}

// -------------------------------------------------------------
// Fetch VERBOSE logs
// -------------------------------------------------------------
async function loadVerboseLogs() {
    try {
        const res = await fetch("/verbose_logs");
        const text = await res.text();

        verboseLines = text.split("\n").filter(line => line.trim().length > 0);
        renderVerboseLogs();

    } catch (err) {
        showError("Failed to load verbose logs: " + err);
    }
}

// -------------------------------------------------------------
// Render MAIN logs with filter
// -------------------------------------------------------------
function applyLogFilter() {
    const filter = document.getElementById("log-filter").value;
    const box = document.getElementById("log-box");

    box.innerHTML = "";

    rawLines.forEach(line => {
        const lower = line.toLowerCase();
        let cls = "info";

        if (lower.includes("error")) cls = "error";
        else if (lower.includes("warn")) cls = "warn";

        if (filter !== "all" && cls !== filter) return;

        const div = document.createElement("div");
        div.className = `entry ${cls}`;
        div.textContent = line;

        box.appendChild(div);
    });

    if (autoScroll) {
        box.scrollTop = box.scrollHeight;
    }
}

// -------------------------------------------------------------
// Render VERBOSE logs (no filter)
// -------------------------------------------------------------
function renderVerboseLogs() {
    const box = document.getElementById("verbose-log-box");
    if (!box) return;

    box.innerHTML = "";

    verboseLines.forEach(line => {
        const div = document.createElement("div");
        div.className = "entry verbose";
        div.textContent = line;
        box.appendChild(div);
    });

    if (autoScroll) {
        box.scrollTop = box.scrollHeight;
    }
}

// -------------------------------------------------------------
// Toggle auto-scroll
// -------------------------------------------------------------
function toggleAutoScroll() {
    autoScroll = document.getElementById("log-autoscroll").checked;
}

// -------------------------------------------------------------
// Refresh BOTH logs
// -------------------------------------------------------------
async function refreshLogs() {
    await loadLogs();
    await loadVerboseLogs();
    showSuccess("Logs refreshed.");
}

// -------------------------------------------------------------
// Tab switching (main / verbose)
// -------------------------------------------------------------
function switchTab(tab) {
    const mainTab = document.getElementById("main-log-tab");
    const verboseTab = document.getElementById("verbose-log-tab");

    const mainBox = document.getElementById("main-log-container");
    const verboseBox = document.getElementById("verbose-log-container");

    if (tab === "main") {
        mainTab.classList.add("active");
        verboseTab.classList.remove("active");

        mainBox.style.display = "block";
        verboseBox.style.display = "none";
    } else {
        verboseTab.classList.add("active");
        mainTab.classList.remove("active");

        verboseBox.style.display = "block";
        mainBox.style.display = "none";
    }
}

// -------------------------------------------------------------
// Auto-load logs when page mounts
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    loadLogs();
    loadVerboseLogs();

    // Hook filter dropdown
    const filter = document.getElementById("log-filter");
    if (filter) {
        filter.onchange = applyLogFilter;
    }

    // Hook auto-scroll checkbox
    const auto = document.getElementById("log-autoscroll");
    if (auto) {
        auto.onchange = toggleAutoScroll;
    }

    // Hook refresh button
    const refreshBtn = document.getElementById("log-refresh");
    if (refreshBtn) {
        refreshBtn.onclick = refreshLogs;
    }

    // Hook tabs
    const mainTab = document.getElementById("main-log-tab");
    const verboseTab = document.getElementById("verbose-log-tab");

    if (mainTab) mainTab.onclick = () => switchTab("main");
    if (verboseTab) verboseTab.onclick = () => switchTab("verbose");
});
