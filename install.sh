#!/bin/bash

MODE="full"

# Parse flags
case "$1" in
    --modules-only)
        MODE="modules"
        ;;
    --update-modules)
        MODE="update"
        ;;
    --termux)
        MODE="termux"
        ;;
    --macos)
        MODE="macos"
        ;;
    *)
        MODE="full"
        ;;
esac

echo "ToyBox Installer Mode: $MODE"

# 1. Ensure git exists
if ! command -v git >/dev/null 2>&1; then
    echo "Error: git is not installed."
    exit 1
fi

# 2. Clone or update repo
if [ ! -d "$HOME/toybox" ]; then
    git clone https://github.com/<YOUR_GITHUB_USERNAME>/toybox.git "$HOME/toybox"
else
    cd "$HOME/toybox"
    git pull
fi

cd "$HOME/toybox"

# 3. Install Python dependencies (Linux default)
if [ "$MODE" = "full" ] || [ "$MODE" = "modules" ] || [ "$MODE" = "update" ]; then
    pip install fastapi uvicorn
fi

# 4. Install active modules
if [ "$MODE" = "full" ] || [ "$MODE" = "modules" ]; then
    for module in modules/*; do
        if [ -f "$module/config.json" ]; then
            enabled=$(grep '"enabled": true' "$module/config.json")
            if [ ! -z "$enabled" ]; then
                bash "$module/install.sh"
            fi
        fi
    done
fi

# 5. Update active modules
if [ "$MODE" = "update" ]; then
    for module in modules/*; do
        if [ -f "$module/config.json" ]; then
            enabled=$(grep '"enabled": true' "$module/config.json")
            if [ ! -z "$enabled" ]; then
                bash "$module/update.sh"
            fi
        fi
    done
fi

# 6. Start ToyBox (full install only)
if [ "$MODE" = "full" ]; then
    uvicorn main:app --host 0.0.0.0 --port 8080
fi
