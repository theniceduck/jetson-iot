# How to Set Up the Project

1. **Clone the Repository**:
   - Run the following command in your terminal:
     ```bash
     git clone https://github.com/theniceduck/jetson-iot.git
     ```
   - If the repository is compressed (e.g., a .zip file), extract it using:
     - **Windows**: Right-click the file and select "Extract All..."
     - **Linux**: Use the command:
       ```bash
       unzip jetson-iot.zip
       ```
     - **Mac**: Double-click the file to extract it.

2. **Rename and Update the `.env` File**:
   - Copy the `.env.example` file and rename it to `.env`.
   - Open the newly created `.env` file in a text editor and update the necessary environment variables.

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
     ```

5. **Enjoy**:
   - Your application should now be running. Access it via the specified ports in either your `.env` or `docker-compose.yaml` file.

