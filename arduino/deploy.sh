#!/bin/bash

# Read config.json
CONNECTION_FILE="../config.json"
CONFIG_FILE="config.json"
TARGET=$(jq -r '.target' "$CONFIG_FILE")
BOARD=$(jq -r '.board' "$CONFIG_FILE")
PORTS=$(jq -r '.arduino.port[]' "$CONNECTION_FILE")
UPLOAD_SPEED=$(jq -r '.arduino.upload_speed' "$CONNECTION_FILE")
PROGRAMMER=$(jq -r '.programmer' "$CONFIG_FILE")

# Compile Arduino image
arduino-cli compile --fqbn "$BOARD" "$TARGET"

# Upload to Arduino board
for PORT in $PORTS; do
    echo "Uploading to Arduino on port: $PORT"
    arduino-cli upload -p "$PORT" --fqbn "$BOARD" "$TARGET"
done
