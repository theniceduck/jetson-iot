#!/bin/bash

# Locate esptool.py
ESPTOOL_PATH=$(find ~/.arduino15/packages/esp32/hardware/esp32 -name esptool.py | head -n 1)

# Check if esptool.py is found
if [ -z "$ESPTOOL_PATH" ]; then
    echo "esptool.py not found! Ensure the ESP32 core is installed using Arduino CLI."
    exit 1
fi

# Find connected ESP32 device port
PORT=$(arduino-cli board list | grep -E "ESP32" | awk '{print $1}')

if [ -z "$PORT" ]; then
    echo "No ESP32 device found. Please connect your ESP32 and try again."
    exit 1
fi

# Erase flash
echo "Erasing flash on port $PORT..."
python3 "$ESPTOOL_PATH" --port "$PORT" erase_flash

if [ $? -eq 0 ]; then
    echo "Flash successfully erased."
else
    echo "Failed to erase flash."
fi