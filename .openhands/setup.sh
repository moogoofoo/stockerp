#!/bin/bash

STARTUP_FILE="/files/startup.sh"
if [ -f "$STARTUP_FILE" ]; then
    source $STARTUP_FILE
fi
