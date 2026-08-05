# ACODE INTEGRATION PLAN — TOYBOX v2.0

This document defines the long‑term plan for integrating the Acode editor engine,
Acode terminal, Acode plugin system, and Termux/proot access into ToyBox v2.0.

It is NOT a module.  
It is NOT a blueprint.  
It is a roadmap for a future subsystem.

---

## 1. GOALS OF ACODE INTEGRATION

ToyBox will eventually support:

- Acode’s Monaco editor engine
- Acode’s terminal (self-contained sandbox)
- Acode’s plugin system (use existing plugins + create new ones)
- Acode’s Termux bridge plugin (control Termux from ToyBox UI)
- Access to Termux filesystem
- Access to Termux proot (Wizard stack)
- Optional: embed Wizard stack inside ToyBox itself

This requires multiple modules working together.

---

## 2. WHY ACODE MUST BE MULTI-MODULE

Acode is not a simple tool.  
It is a mini IDE ecosystem.

ToyBox v2.0 is designed for **small, isolated modules**, not monolithic ones.

Therefore, Acode integration must be split into **five modules**:

1. System Monitor Module  
2. Vault Module  
3. Editor Core Module (Monaco)  
4. File System Bridge Module  
5. Acode Integration Module

Each module handles a specific part of the system.

---

## 3. MODULE BREAKDOWN

### 3.1 SYSTEM MONITOR MODULE
Provides:
- Logs
- Errors
- Performance metrics
- Terminal output capture
- Module runtime output

Required before adding a terminal engine.

---

### 3.2 VAULT MODULE
Provides:
- Secure storage
- Editor settings
- Plugin settings
- Terminal profiles
- Sandbox rules
- Wizard stack config

Acode plugins need persistent storage — Vault handles that.

---

### 3.3 EDITOR CORE MODULE (MONACO)
Provides:
- Monaco editor engine
- Acode core JS
- Syntax highlighting
- Basic editor UI
- No file operations yet
- No terminal yet
- No plugins yet

This is the “engine only.”

---

### 3.4 FILE SYSTEM BRIDGE MODULE
Provides:
- File open/save
- File tree
- Directory listing
- Sandbox rules
- Termux filesystem access
- Termux proot access (Wizard stack)
- Backend endpoints for editor operations

Endpoints include:
- `/editor/open`
- `/editor/save`
- `/editor/tree`
- `/editor/fs`
- `/editor/proot`
- `/editor/termux`

This is the glue between ToyBox, Termux, and Acode.

---

### 3.5 ACODE INTEGRATION MODULE
Provides:
- Acode terminal
- Acode plugin system
- Acode command palette
- Acode sidebar
- Acode themes
- Acode extensions
- Acode file explorer
- Acode terminal → Termux bridge plugin
- Acode terminal → ToyBox backend bridge
- Acode terminal → Wizard stack access

This is where ToyBox becomes a full IDE.

---

## 4. TERMUX + PROOT + WIZARD STACK ACCESS

ToyBox will support three access methods:

### 4.1 Through Acode Terminal Plugin
Acode terminal → Termux → proot → Wizard stack  
Full access to your existing environment.

### 4.2 Through ToyBox File System Bridge
ToyBox → backend → Termux → proot → Wizard stack  
Backend-level control.

### 4.3 Embedded Wizard Stack (Optional)
Wizard stack installed inside ToyBox’s own sandbox:
- No Termux required
- Fully self-contained
- Controlled via ToyBox terminal

Advanced but possible.

---

## 5. PLUGIN SUPPORT

ToyBox will support:

- Existing Acode plugins
- Acode terminal plugin
- Acode file explorer plugin
- Acode Git plugin
- Acode LSP plugins
- Acode theme plugins
- Acode sidebar plugins
- Custom ToyBox plugins

Plugins are simple:
- JS bundles
- JSON manifests
- Optional HTML/CSS
- Optional backend calls

ToyBox can load them exactly like Acode.

---

## 6. RECOMMENDED BUILD ORDER

1. System Monitor Module  
2. Vault Module  
3. Editor Core Module  
4. File System Bridge Module  
5. Acode Integration Module  

This order keeps ToyBox stable and prevents monolithic module bloat.

---

## 7. STATUS

This plan is **not started**.  
It is documented for future development.  
ToyBox v2.0 must remain stable before beginning this subsystem.

