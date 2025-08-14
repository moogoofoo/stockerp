#!/bin/bash

STARTUP_FILE="/files/startup.sh"
if [ -f "$ENV_FILE" ]; then
    source /files/startup.sh
fi
