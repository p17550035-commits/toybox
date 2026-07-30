# toybox
Fully modular toolbox

# ToyBox Installer (Linux First)
visit the website for easier copy links
https://p17550035-commits.github.io/toybox/

## Overview
The ToyBox installer allows any Linux system to fully rebuild ToyBox from scratch using a single command copied directly from this README. It automatically creates the folder tree, installs dependencies, pulls the GitHub repository, installs active modules, and sets up the environment with zero manual configuration.

This installer is designed to be simple, modular, and future‑proof. As ToyBox grows, additional OS installers (Windows, macOS, Android/Termux, iOS) can be added to this README using the same pattern.

---

## One‑Line Install Command (Linux)

Copy and paste this into any Linux terminal:

```curl -s https://raw.githubusercontent.com/p17550035-commits/toybox/main/install.sh | bash```

This command will:
- Download the installer script directly from GitHub
- Execute it automatically
- Build the entire ToyBox environment
- Install active modules
- Start the ToyBox server

---

## Installer Responsibilities

The installer performs the following steps in order:

### 1. Check for git
ToyBox requires Git to pull the repository.  
If Git is missing, the installer will notify the user and stop.

### 2. Clone or update the ToyBox repo

If ToyBox is not installed:

```git clone https://github.com/p17550035-commits/toybox.git ~/toybox```

If ToyBox already exists:

cd ~/toybox  
git pull

This ensures the system always uses the latest version of ToyBox.

### 3. Create the folder tree

The installer ensures the following structure exists:

toybox/  
    main.py  
    router.py  
    loader.py  
    toggles.py  
    modules/  
    ui/

Missing folders are created automatically.

### 4. Install Python + dependencies

The installer ensures the following are installed:

- python3  
- pip  
- fastapi  
- uvicorn  
- any module‑specific dependencies  

### 5. Install active modules

For each module inside `modules/`:

1. Read its config.json  
2. If "enabled": true  
3. Run its install.sh script  

### 6. Start ToyBox

The installer launches the ToyBox server:

uvicorn main:app --host 0.0.0.0 --port 8080

### 7. Print the UI URL

After installation, the installer prints:

ToyBox UI available at:  
http://localhost:8080/ui

---

## Installer Script (Skeleton)

The final install.sh follows this structure:

#!/bin/bash  
# 1. Check for git  
# 2. Clone or update repo  
# 3. Create folder tree  
# 4. Install Python + dependencies  
# 5. Install active modules  
# 6. Start ToyBox  

The full version is implemented in install.sh at the root of this repository.

---

## Cross‑OS Strategy (Future)

Once the Linux installer is stable, additional installers will be added to this README.

### Windows (PowerShell)

```Invoke-WebRequest https://raw.githubusercontent.com/p17550035-commits/toybox/main/install.ps1 -UseBasicParsing | Invoke-Expression```

### macOS (bash/zsh)

```curl -s https://raw.githubusercontent.com/p17550035-commits/toybox/main/install_mac.sh | bash```

### Android / Termux

```curl -s https://raw.githubusercontent.com/p17550035-commits/toybox/main/install_termux.sh | bash```

### iOS (Pythonista / Pyto)

A Python installer snippet will be added for iOS users once the mobile build is ready.

---

## Notes

- The installer must remain simple and modular.  
- The installer must never modify module logic.  
- Only active modules (enabled: true) are installed or updated.  
- The installer always pulls the latest version of ToyBox.  
- The installer rebuilds the folder tree if missing.  
- The Linux installer is the primary supported installer at this stage.

---

## Summary

The ToyBox installer ensures that any Linux machine can rebuild ToyBox from scratch using a single command from this README. As ToyBox grows, additional OS installers will be added without changing the core Linux installer. This keeps ToyBox portable, modular, and easy to deploy anywhere.
