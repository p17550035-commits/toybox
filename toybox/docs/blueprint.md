# ============================================================
# TOYBOX BLUEPRINT (FINAL, STABLE, NON‑CHANGING)
# ============================================================

## I. Core Philosophy
- Main app is a router + loader, nothing else.
- Modules live in their own folders, never touching main.py.
- Loader only loads ACTIVE modules.
- Toggles determine active modules.
- Toggles trigger install/uninstall/update scripts.
- Modules stay separate and self-contained.
- UI controls installation, toggling, updating, running.
- CAT-method file writes keep everything predictable.
- Config.json stores ALL module settings.

## II. Folder Structure (Final)
toybox/
    main.py
    router.py
    loader.py
    toggles.py
    modules/
        <module_name>/
            module.py
            install.sh
            uninstall.sh
            update.sh
            config.json
    ui/
        index.html
        module_installer.html
        module_toggle.html
        module_config.html
        module_runner.html

## III. Main Components

### 1. main.py
- Starts FastAPI.
- Includes router.
- Never changes again.

### 2. router.py
- Central wiring point.
- Endpoints:
    - /modules
    - /run/<module>
    - /toggle/<module>
    - /install
    - /uninstall
    - /update/<module>
    - /config/<module>
    - /ui
- Never touches module internals.

### 3. loader.py
- Reads toggles.
- Loads only active modules.
- Dynamically imports module.py.
- Passes config settings into module.run().
- Never modifies config.json.

### 4. toggles.py
- Stores toggle states.
- Thread-safe.
- Persistent.
- When toggled ON:
    - run install.sh
    - set enabled=true in config.json
- When toggled OFF:
    - run uninstall.sh
    - set enabled=false in config.json
- When active:
    - update button visible
    - update.sh can be triggered

### 5. modules/<name>/
Each module is fully isolated:
- module.py → logic only
- install.sh → dependency setup
- uninstall.sh → cleanup
- update.sh → updates, migrations, patches
- config.json → settings, flags, metadata

## IV. Toggle System Rules

### When toggled ON:
1. Run install.sh
2. Set "enabled": true in config.json
3. Loader loads module
4. UI shows module

### When toggled OFF:
1. Run uninstall.sh
2. Set "enabled": false in config.json
3. Loader unloads module
4. UI hides module

### When active:
- Update button appears
- update.sh can run

## V. Module Config System

### config.json example:
{
    "name": "echo",
    "version": "1.0",
    "enabled": false,
    "settings": {
        "requires_text": true,
        "max_length": 200
    }
}

### Loader responsibilities:
- Read config.json
- Only load modules where enabled=true
- Pass settings into module.run(args, settings)

### Toggle system responsibilities:
- Modify enabled flag
- Trigger install/uninstall scripts

### UI responsibilities:
- Display config settings
- Allow editing config.json
- Send changes to router

## VI. UI Responsibilities
- Install new modules
- Toggle modules on/off
- Update modules
- Edit config.json
- Run modules
- Display output
- Never modify backend files directly

## VII. Non-Negotiable Rules
- main.py stays clean forever.
- Modules stay separate forever.
- Loader only loads active modules.
- Toggle system controls environment.
- UI is the only place modules are created.
- No file drift.
- No overloading.
- No plugin hell.
- No Termux pain.

- ## Installer Workflow Options
- 
These are the three workflow options used after setting up the installer and README. They define how development continues entirely inside GitHub, avoiding Termux issues and keeping the project clean and modular.

## Option 1 — Generate install.sh (Skeleton)
Create the initial install.sh script inside the repo.  
This script will:
- Build the folder tree
- Install dependencies
- Install active modules
- Start ToyBox

This is the foundation for the one‑line installer in README.md.

## Option 2 — Generate README.md Installer Section
Add the one‑line installer command to README.md:

curl -s https://raw.githubusercontent.com/<YOUR_GITHUB_USERNAME>/toybox/main/install.sh | bash

This allows ToyBox to be installed on any Linux system using a single copy‑paste command.

## Option 3 — Integrate Installer Into Task List
Add installer tasks to the main project task list:
- Create installer blueprint
- Create install.sh
- Add GitHub sync logic
- Test installer on clean system
- Test module auto‑install
- Test update.sh via installer
- Lock installer
- Document installer rules

This ensures the installer becomes part of the official ToyBox development workflow.
