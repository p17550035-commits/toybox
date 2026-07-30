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

# ============================================================
# TOYBOX TASK LIST (FOLLOW IN ORDER, NO DRIFT)
# ============================================================

## PHASE 1 — Skeleton
1. Create folder structure
2. Create main.py
3. Create router.py
4. Create loader.py
5. Create toggles.py

## PHASE 2 — Module System
6. Create module template
7. Create install/uninstall script templates
8. Create config.json template
9. Add config loader logic
10. Create update.sh template
11. Add update endpoint

## PHASE 3 — UI
12. Create module installer UI
13. Create module toggle UI
14. Create module config editor UI
15. Create module update button UI
16. Create module runner UI

## PHASE 4 — Integration
17. Connect UI to router
18. Test module installation
19. Test toggles
20. Test config system
21. Test update system
22. Test module execution

## PHASE 5 — First Real Tools
23. Add your first real module
24. Add second module
25. Add system monitor module
26. Add vault module

## PHASE 6 — Stability
27. Lock skeleton
28. Document module rules
29. Document toggle rules
30. Document config rules
