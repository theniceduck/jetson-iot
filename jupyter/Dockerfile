# Base Jupyter image
FROM jupyter/base-notebook:latest

# Switch to root to install Arduino CLI
USER root

# Install Arduino CLI
RUN wget https://github.com/arduino/arduino-cli/releases/download/v1.1.1/arduino-cli_1.1.1_Linux_64bit.tar.gz && \
    tar -xvzf arduino-cli_1.1.1_Linux_64bit.tar.gz && \
    mv arduino-cli /usr/local/bin/arduino-cli && \
    rm arduino-cli_1.1.1_Linux_64bit.tar.gz

# Create Arduino CLI config directory
RUN mkdir -p /home/jupyter/.arduino15

# Switch back to the default user
USER jovyan

# Set up environment variable for Arduino CLI
ENV ARDUINO_CLI_CONFIG=/home/jupyter/.arduino15/arduino-cli.yaml
