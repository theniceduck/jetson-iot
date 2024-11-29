#!/bin/bash

echo "Creating virtual environment..."
python3 -m venv venv
echo "Sourcing virtual environment..."
source venv/bin/activate
echo "Installing requirements..."
pip install -r requirements.txt
read -p "Success..."
