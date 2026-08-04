async function refreshStatus() {
    try {
        const res = await fetch("/modules/status/run");
        const json = await res.json();

        document.getElementById("uptime").textContent =
            "Uptime: " + json.uptime + "s";

        document.getElementById("modules").textContent =
            "Modules: " + json.modules.join(", ");

        document.getElementById("toggles").textContent =
            "Toggles: " + JSON.stringify(json.toggles);
    } catch (e) {
        console.error("Status refresh failed:", e);
    }
}

setInterval(refreshStatus, 1000);
refreshStatus();
