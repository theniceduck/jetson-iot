#!/bin/bash

source venv/bin/activate
echo "Starting yolov8 object detection..."
python3 yolov8_detection.py
read -p "Success..."