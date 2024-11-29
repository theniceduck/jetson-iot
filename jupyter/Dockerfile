# Base Jupyter image
FROM quay.io/jupyter/base-notebook:latest

# Switch to root to install additional dependencies
USER root

# Install Arduino CLI, screen, and other dependencies
RUN wget https://github.com/arduino/arduino-cli/releases/download/v1.1.1/arduino-cli_1.1.1_Linux_ARM64.tar.gz && \
    tar -xvzf arduino-cli_1.1.1_Linux_ARM64.tar.gz && \
    mv arduino-cli /usr/local/bin/arduino-cli && \
    rm arduino-cli_1.1.1_Linux_ARM64.tar.gz && \
    apt-get update && \
    apt-get install -y screen git && \
    apt-get remove --purge -y brltty && \
    rm -rf /var/lib/apt/lists/*

# Create Arduino CLI config directory
RUN mkdir -p /home/jupyter/.arduino15

# Switch back to the default user
USER jovyan

# Set up environment variable for Arduino CLI
ENV ARDUINO_CLI_CONFIG=/home/jupyter/.arduino15/arduino-cli.yaml
