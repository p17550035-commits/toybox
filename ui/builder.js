async function createModule() {
    const data = {
        name: document.getElementById("name").value,
        description: document.getElementById("description").value,
        category: document.getElementById("category").value,
        page_type: document.getElementById("page_type").value,
        code: document.getElementById("code").value,
        install_script: document.getElementById("install_script").value,
        uninstall_script: document.getElementById("uninstall_script").value,
        config_data: document.getElementById("config_data").value
    };

    const res = await fetch("/builder/create", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
    });

    const json = await res.json();
    alert(json.message || "Module created.");
}

async function deleteModule() {
    const name = document.getElementById("delete_name").value;

    const res = await fetch("/builder/delete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name })
    });

    const json = await res.json();
    alert(json.message || "Module deleted.");
}
