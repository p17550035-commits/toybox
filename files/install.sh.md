# ToyBox Installer (Linux First)

## Overview
This installer is designed to let any Linux system fully rebuild ToyBox from scratch using a single command copied directly from the README.md. It creates the folder tree, installs dependencies, pulls the GitHub repo, installs active modules, and sets up the environment automatically.

Later, additional OS installers (Windows, macOS, Android/Termux, iOS) can be added to the README.md using the same pattern.

## One‑Line Install Command (Linux)
Copy and paste this into any Linux terminal:

curl -s https://raw.githubusercontent.com/<YOUR_GITHUB_USERNAME>/toybox/main/install.sh | bash

This command will:
1. Download the installer script from GitHub.
2. Execute it automatically.
3. Build the entire ToyBox environment.

## Installer Responsibilities
The installer performs the following steps:

1. **Check for git**
   - If missing, prompt user to install it.

2. **Clone or update the ToyBox repo**
   - If ~/toybox does not exist:
     git clone https://github.com/<YOUR_GITHUB_USERNAME>/toybox.git
   - If it does exist:
     cd toybox && git pull

3. **Create folder tree**
   Ensures the following structure exists:
   toybox/
       main.py
       router.py
       loader.py
       toggles.py
       modules/
       ui/

4. **Install Python + dependencies**
   - python3
   - pip
   - fastapi
   - uvicorn
   - any module‑specific dependencies

5. **Install active modules**
   For each module folder:
   - Read config.json
   - If "enabled": true:
       bash install.sh

6. **Start ToyBox**
   uvicorn main:app --host 0.0.0.0 --port 8080

7. **Print UI URL**
   http://localhost:8080/ui

## Installer Script (Skeleton)
This is the structure the final install.sh will follow:

#!/bin/bash

# 1. Check for git
# 2. Clone or update repo
# 3. Create folder tree
# 4. Install Python + dependencies
# 5. Install active modules
# 6. Start ToyBox

## Cross‑OS Strategy (Future)
Once the Linux installer is stable, additional installers can be added to README.md:

### Windows (PowerShell)
Invoke-WebRequest https://raw.githubusercontent.com/<YOU>/toybox/main/install.ps1 -UseBasicParsing | Invoke-Expression

### macOS (bash/zsh)
curl -s https://raw.githubusercontent.com/<YOU>/toybox/main/install_mac.sh | bash

### Android/Termux
curl -s https://raw.githubusercontent.com/<YOU>/toybox/main/install_termux.sh | bash

### iOS (Pythonista/Pyto)
Copy/paste Python installer snippet into Pythonista/Pyto.

## Notes
- Installer must remain simple and modular.
- Installer must never modify module logic.
- Installer must only run install.sh for active modules.
- Installer must always pull the latest repo version.
- Installer must always rebuild the folder tree if missing.

## Summary
This installer system ensures ToyBox can be rebuilt on any Linux machine using a single command from README.md. As ToyBox grows, additional OS installers can be added without changing the core Linux installer.
