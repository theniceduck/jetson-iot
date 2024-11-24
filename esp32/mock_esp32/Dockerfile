FROM python:3.9-slim

# Set up the working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the Flask application
CMD ["python3", "mock_esp32.py"]
