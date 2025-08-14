#!/bin/bash
set -e    # Exit immediately on any error
set -x    # Print each command as it runs for debugging

LOG_FILE="/tmp/setup.log"
echo "[setup] Starting setup.sh" | tee -a "$LOG_FILE"

# === Load environment variables safely ===
ENV_FILE=".openhands/env"
if [ -f "$ENV_FILE" ]; then
    echo "[setup] Loading env vars from $ENV_FILE" | tee -a "$LOG_FILE"
    while IFS='=' read -r key value; do
        # Skip blank lines or comments
        [[ -z "$key" || "$key" =~ ^# ]] && continue
        # Export for current script
        export "$key"="$value"
        # Append to /etc/environment so new shells in sandbox pick it up
        echo "$key=\"$value\"" | sudo tee -a /etc/environment
    done < "$ENV_FILE"
fi

# === Install required packages ===
echo "[setup] Updating package lists" | tee -a "$LOG_FILE"
sudo apt-get update -y 2>&1 | tee -a "$LOG_FILE"

echo "[setup] Installing lsof" | tee -a "$LOG_FILE"
sudo apt-get install -y lsof 2>&1 | tee -a "$LOG_FILE"

# === Frontend setup ===
if [ -d "frontend" ]; then
    echo "[setup] Installing frontend dependencies" | tee -a "$LOG_FILE"
    cd frontend
    npm install 2>&1 | tee -a "$LOG_FILE"
    cd ..
fi

echo "[setup] setup.sh completed successfully" | tee -a "$LOG_FILE"
