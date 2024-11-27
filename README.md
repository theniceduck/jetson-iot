# How to Set Up the Project

1. **Clone the Repository**:
   - Run the following command in your terminal:
     ```bash
     git clone https://github.com/theniceduck/jetson-iot.git
     ```

2. **Rename and Update the Configuration File**:
   - Rename `config.h.example` to `config.h`:
     ```bash
     mv esp32/esp32/config.h.example esp32/esp32/config.h
     ```
   - Open `config.h` in a text editor and fill in the necessary details as per your project requirements.

   - Upload `esp32/esp32.ino` to the ESP32 device.

3. **Install Docker and Docker Compose**:
   - For **Windows** and **Mac**, download and install [Docker Desktop](https://www.docker.com/products/docker-desktop).
   - For **Linux**, install Docker and Docker Compose using your package manager. For example, on Ubuntu:
     ```bash
     sudo apt-get update
     sudo apt-get install docker.io docker-compose
     ```
   - Ensure Docker is set to use the WSL2 based engine if you are on Windows.

4. **Run the Application**:
   - Navigate to the project directory in your terminal and run:
     ```bash
     docker-compose up -d --build
     # If using the Compose plugin, use the following command:
     docker compose up -d --build
     ```

5. **Enjoy**:
   - Your application should now be running. Access it via the specified ports in either your `.env` or `docker-compose.yaml` file.
   
6. **Manage Docker Containers**:
   - To stop the running containers momentarily, use the following command:
     ```bash
     docker-compose stop
     ```
   - To remove the container along with its associated volumes, use:
     ```bash
     docker-compose down -v
     ```
   - This command will stop the containers and remove them, along with any volumes defined in the `docker-compose.yaml` file.

