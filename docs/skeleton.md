# TOYBOX SKELETON v2.0 — SYSTEM WIRING AND FLOW

This document explains how the ToyBox v2.0 skeleton is wired together:
how processes start, how modules are loaded, how the UI is generated,
and how everything talks to everything else.

It is the technical “map” of the system.

---

## 1. HIGH-LEVEL FLOW

At a high level, ToyBox v2.0 works like this:

1. The Python backend starts (`main.py`).
2. Global settings and toggles are loaded.
3. Modules are discovered and loaded.
4. Navigation and UI metadata are generated.
5. The HTTP server starts and exposes endpoints.
6. The browser UI connects to those endpoints.
7. Modules are installed, toggled, configured, and executed via the UI.

Everything in the skeleton exists to support that flow.

---

## 2. CORE FILES AND RESPONSIBILITIES

### 2.1 main.py — Entry Point

**Role:** Bootstraps the entire system.

Main responsibilities:

- Initialize logging and environment.
- Load global settings (from `core/settings.py`).
- Load toggle state (from `toggles.py`).
- Initialize module loader (from `loader.py` / `core/modules_api.py`).
- Initialize builder API (from `core/builder_api.py`).
- Wire up the router (from `router.py`).
- Start the HTTP server (FastAPI / similar).

`main.py` does **not** contain business logic.  
It is a coordinator that wires together the core subsystems.

### 2.2 router.py — Endpoints and Routing

**Role:** Defines all HTTP endpoints.

Typical endpoint groups:

- `/modules` — list, info, actions on modules.
- `/module/install` — install a module.
- `/module/uninstall` — uninstall a module.
- `/module/run` — execute a module’s `run.py`.
- `/toggles` — get/set toggle states.
- `/builder` — generate new modules.
- `/settings` — read/write global settings.
- `/nav` — return navigation structure for the UI.

`router.py` does **not** implement logic directly.  
It calls into:

- `core/modules_api.py`
- `core/builder_api.py`
- `toggles.py`
- `core/settings.py`
- `page_loader.py` (for UI pages, if used)

### 2.3 loader.py — Module Discovery and Loading

**Role:** Find modules and load their metadata/config.

Responsibilities:

- Scan `modules/` for module folders.
- Read `metadata.json` for each module.
- Read `config.json` for each module.
- Validate basic structure (HTML/JS/CSS, `run.py`, scripts).
- Build an internal registry of modules.

This registry is used by:

- `core/modules_api.py` (for lifecycle operations).
- `router.py` (for listing modules and serving module info).
- Navigation generation (for Tools page and module pages).

### 2.4 toggles.py — Unified Toggle System

**Role:** Manage boolean feature/module toggles.

Responsibilities:

- Load toggle state from a JSON file (e.g. `config/toggles.json`).
- Provide functions to get/set toggles.
- Expose toggle operations to the router.
- Ensure toggles are always boolean and documented.

The UI uses these toggles to show/hide modules, features, or pages.

### 2.5 core/builder_api.py — Module Generation

**Role:** Create new modules programmatically.

Responsibilities:

- Generate module folder structure under `modules/`.
- Create `module.html`, `module.js`, `module.css`.
- Create `run.py` with a standard entrypoint.
- Create `config.json` with sane defaults.
- Create `metadata.json` with name, description, tags, etc.
- Optionally create `install.sh` and `uninstall.sh`.

The builder is invoked via:

- Router endpoints (e.g. `/builder/create`).
- The Builder UI page (user-facing).

### 2.6 core/modules_api.py — Module Lifecycle

**Role:** Provide a clean API for module operations.

Responsibilities:

- Install modules (run `install.sh` if present).
- Uninstall modules (run `uninstall.sh` if present).
- Execute modules (`run.py`).
- Read/write module config.
- Expose module status (installed, enabled, etc).

`router.py` calls `modules_api` instead of touching modules directly.

### 2.7 core/settings.py — Global Settings

**Role:** Centralize global configuration.

Responsibilities:

- Load settings from a file (e.g. `config/settings.json`).
- Provide accessors for important values (ports, paths, flags).
- Ensure defaults exist and are safe.

`main.py` and `router.py` rely on `core/settings.py` for configuration.

### 2.8 page_loader.py — UI Page Loader

**Role:** Serve static UI pages and assets.

Responsibilities:

- Map routes (e.g. `/dashboard`, `/builder`, `/tools`) to HTML files.
- Serve CSS and JS assets.
- Optionally generate or modify navigation metadata.

This keeps UI file handling separate from business logic.

---

## 3. FOLDER STRUCTURE AND HOW IT CONNECTS

### 3.1 Root Layout

At the top level:

- `main.py` — entry point.
- `router.py` — endpoints.
- `loader.py` — module discovery.
- `toggles.py` — toggle system.
- `page_loader.py` — UI page serving.
- `core/` — core APIs and settings.
- `modules/` — actual modules.
- `ui/` — UI assets (if separated).
- `config/` — JSON configs.
- `reset`, `reset_nav` — helper scripts.

Each of these plays a specific role in the boot and runtime flow.

### 3.2 core/ Folder

Contains:

- `builder_api.py`
- `modules_api.py`
- `settings.py`

This folder is the “backend brain” of ToyBox.  
All high-level operations go through these APIs.

### 3.3 modules/ Folder

Each module lives in its own folder:

- `modules/<module_name>/module.html`
- `modules/<module_name>/module.js`
- `modules/<module_name>/module.css`
- `modules/<module_name>/run.py`
- `modules/<module_name>/config.json`
- `modules/<module_name>/metadata.json`
- `modules/<module_name>/install.sh`
- `modules/<module_name>/uninstall.sh`

The skeleton assumes:

- Modules are self-contained.
- Modules do not modify core files.
- Modules interact via defined APIs and endpoints.

### 3.4 config/ Folder

Holds JSON configuration files:

- `config/settings.json` — global settings.
- `config/toggles.json` — toggle states.
- Potential future configs (themes, permissions, etc).

This keeps configuration out of code and easy to edit.

---

## 4. BOOT SEQUENCE IN DETAIL

The boot sequence is:

1. **Start main.py**
   - Initialize logging.
   - Load global settings via `core/settings.py`.
   - Load toggles via `toggles.py`.

2. **Load Modules**
   - Call `loader.py` to scan `modules/`.
   - Build a registry of modules (metadata + config).
   - Pass this registry to `core/modules_api.py`.

3. **Wire Router**
   - Initialize `router.py` with references to:
     - `core/modules_api.py`
     - `core/builder_api.py`
     - `toggles.py`
     - `core/settings.py`
   - Register endpoints for modules, builder, toggles, settings, nav.

4. **Prepare UI**
   - Use `page_loader.py` to map routes to HTML pages.
   - Optionally generate navigation metadata for the UI.

5. **Start HTTP Server**
   - Start FastAPI (or similar) app.
   - Bind to host/port from `core/settings.py`.

6. **Client Connects**
   - Browser opens Dashboard, Tools, Builder, etc.
   - UI calls router endpoints to:
     - List modules.
     - Install/uninstall modules.
     - Toggle modules.
     - Edit config.
     - Run modules.

---

## 5. HOW MODULES ARE WIRED IN

### 5.1 Module Discovery

- `loader.py` scans `modules/`.
- For each folder, it expects:
  - `metadata.json`
  - `config.json`
  - `run.py`
  - UI files (HTML/JS/CSS)

If a module is missing critical files, it can be skipped or flagged.

### 5.2 Module Registry

`loader.py` builds a registry like:

- Name
- ID
- Description
- Tags
- Paths to files
- Config schema
- Status (installed, enabled, etc)

This registry is passed to `core/modules_api.py`.

### 5.3 Module Operations

When the UI or router wants to act on a module:

- Install:
  - Call `modules_api.install(module_id)`
  - Run `install.sh` if present.
- Uninstall:
  - Call `modules_api.uninstall(module_id)`
  - Run `uninstall.sh` if present.
- Run:
  - Call `modules_api.run(module_id)`
  - Execute `run.py` with a defined interface.
- Config:
  - Read/write `config.json` via `modules_api`.

Modules never directly touch core files.  
They operate through the APIs and endpoints.

---

## 6. UI WIRING

### 6.1 Pages

Core pages:

- Dashboard — overview, status, module cards.
- Builder — create new modules.
- Logs — view system/module logs.
- Settings — global settings.
- Tools — list and manage modules.
- Module pages — per-module UI.

Each page is backed by:

- HTML (structure)
- CSS (styling)
- JS (logic, API calls)

### 6.2 Navigation

Navigation is generated based on:

- Core pages (Dashboard, Builder, etc).
- Module metadata (for module-specific pages).
- Toggle states (to show/hide features).

The UI calls a nav endpoint (e.g. `/nav`) to get the structure.

### 6.3 API Calls

The UI talks to the backend via:

- JSON endpoints (router).
- Standardized responses (success, error, data).

Examples:

- GET `/modules` → list modules.
- POST `/module/install` → install module.
- POST `/module/uninstall` → uninstall module.
- POST `/module/run` → run module.
- GET `/toggles` → get toggles.
- POST `/toggles` → set toggles.
- GET `/settings` → get settings.
- POST `/settings` → update settings.
- POST `/builder/create` → create module.

---

## 7. TOGGLES AND CONFIG — HOW THEY INTERACT

### 7.1 Toggles

Toggles are:

- Boolean flags stored in JSON.
- Used to enable/disable modules or features.
- Managed by `toggles.py` and exposed via router.

The UI can:

- Read toggle states.
- Flip toggles.
- Reflect changes immediately (e.g. hide/show modules).

### 7.2 Config

Config files:

- Per-module (`config.json`).
- Global (`config/settings.json`).

They define:

- Defaults.
- Behavior.
- Limits.
- Options.

`core/modules_api.py` and `core/settings.py` provide safe accessors.

---

## 8. RESET SCRIPTS

### 8.1 reset

A helper script to:

- Clear certain state.
- Reset modules or configs.
- Reinitialize parts of the system.

### 8.2 reset_nav

A helper script to:

- Regenerate navigation.
- Clear stale nav data.
- Fix UI routing issues.

These scripts are used when the skeleton or nav structure changes.

---

## 9. DESIGN PRINCIPLES

ToyBox v2.0 skeleton is built around:

- **Modularity:** Modules are self-contained.
- **Separation of concerns:** Core APIs, router, UI, modules, config are separated.
- **Predictability:** Folder structure and APIs are consistent.
- **Safety:** Modules cannot modify core files.
- **Extensibility:** Builder can generate new modules easily.
- **Transparency:** Docs (`blueprintsV2.md`, `tasksV2.md`, `skeleton.md`) explain the system.

---

## 10. HOW TO EXTEND THE SKELETON

To extend ToyBox v2.0 safely:

1. Add new modules under `modules/` using the builder.
2. Add new endpoints in `router.py` that call into core APIs.
3. Add new pages in the UI and wire them via `page_loader.py`.
4. Add new config files under `config/` and access them via `core/settings.py` or new APIs.
5. Keep core files stable and documented in `blueprintsV2.md` and `skeleton.md`.

This skeleton is the foundation.  
Modules and features grow on top of it.

