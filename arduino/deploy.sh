#!/bin/bash

# Read config.json
CONNECTION_FILE="../config.json"
CONFIG_FILE="config.json"
TARGET=$(jq -r '.target' "$CONFIG_FILE")
BOARD=$(jq -r '.board' "$CONFIG_FILE")
PORT=$(jq -r '.arduino.port' "$CONNECTION_FILE")
UPLOAD_SPEED=$(jq -r '.arduino.upload_speed' "$CONNECTION_FILE")
PROGRAMMER=$(jq -r '.programmer' "$CONFIG_FILE")

# Compile Arduino image
arduino-cli compile --fqbn "$BOARD" "$TARGET"

# Upload to Arduino board
arduino-cli upload -p "$PORT" --fqbn "$BOARD" "$TARGET"
