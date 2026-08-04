TOYBOX BLUEPRINT V2 — CURRENT SYSTEM (SKELETON v2.0)

This blueprint describes ToyBox exactly as it exists in the v2.0 skeleton.
The next evolution (blueprints_v2.1.md) will build on this file.

1. SYSTEM OVERVIEW
ToyBox v2.0 is a modular tool platform built around:
Stable backend skeleton
Dynamic module system
Unified builder
Generated navigation
Dashboard-style UI
Lifecycle and toggle system
Predictable folder structure
Consistent module API

2. FOLDER STRUCTURE
main.py
router.py
loader.py
toggles.py
core/
modules/
ui/
config/
page_loader.py
reset
reset_nav

3. BACKEND ARCHITECTURE
main.py starts server and loads settings and modules
router.py handles endpoints
loader.py loads modules and metadata
toggles.py manages toggle states
core/builder_api.py generates modules
core/modules_api.py handles module lifecycle
core/settings.py loads global settings

4. MODULE SYSTEM
Each module contains:
HTML, JS, CSS
run.py
config.json
metadata.json
install.sh
uninstall.sh

Modules must be self-contained and must not modify core files.

5. UI SYSTEM
Dashboard
Builder
Logs
Settings
Tools
Module pages

Navigation is generated automatically.

6. LIFECYCLE SYSTEM
Boot main.py
Load settings
Load toggles
Load modules
Generate navigation
Start UI
Serve module endpoints

7. TOGGLE SYSTEM
Stored in JSON
Managed by toggles.py and UI
Must be boolean

8. CONFIG SYSTEM
Each module has config.json
Loaded by loader and modules_api
Must be valid JSON

9. BUILDER SYSTEM
Creates module folders
Generates HTML, JS, CSS
Writes metadata.json and config.json
Integrates with navigation
Uses template modes and overrides

10. INSTALLER SYSTEM (PARTIAL)
Create installer blueprint
Create install.sh
Add GitHub sync logic
Test on clean system
Test module auto-install
Test update.sh via installer
Lock installer
Document installer rules

11. CURRENT STATUS
ToyBox v2.0 is stable, modular, documented, and ready for real modules.

12. NEXT STEPS FOR BLUEPRINT v2.1
Full installer system
Module permissions
Module settings pages
Module icons and packs
Themes and advanced dashboard
Auto-update and dependency handling
Module sandboxing
