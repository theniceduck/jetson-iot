#!/bin/bash

echo "Creating virtual environment..."
python3 -m venv venv
echo "Installing requirements..."
pip3 install -r requirements.txt
