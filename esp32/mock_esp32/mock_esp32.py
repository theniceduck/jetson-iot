from flask import Flask, jsonify
import random
import time
import threading
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


# Flask setup
app = Flask(__name__)

# Mock state of the LED
led_state = {"status": "OFF"}

# InfluxDB configuration
INFLUXDB_URL = "http://influxdb:8086"  # Update with your InfluxDB URL
INFLUXDB_TOKEN = "lmSuJ5EyZ6g1oGKl_RlmBtou_WUCRoPFMbhqLYzGxf3U1JTCWt_B1cWeHYKXOztbDzm3blB2MJmfunrgORAgWA=="  # Replace with your token
INFLUXDB_ORG = "cairo"  # Replace with your organization name
INFLUXDB_BUCKET = "bucket1"  # Replace with your bucket name

# Initialize InfluxDB client
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Start time for calculating elapsed time
start_time = time.time()

# Mock state of the LED
led_state = {"status": "OFF"}

@app.route("/ledon", methods=["GET"])
def led_on():
    global led_state
    led_state["status"] = "ON"
    return jsonify({"message": "LED turned ON", "led_state": led_state})

@app.route("/ledoff", methods=["GET"])
def led_off():
    global led_state
    led_state["status"] = "OFF"
    return jsonify({"message": "LED turned OFF", "led_state": led_state})

@app.route("/getstate", methods=["GET"])
def get_state():
    return jsonify({"led_state": led_state})

# Function to generate and upload data every 10 seconds
def generate_data_periodically():
    while True:
        # Calculate elapsed time since the application started
        elapsed_time = round((time.time() - start_time) / 3600, 2)  # Elapsed time in hours

        # Generate random temperature and humidity
        temperature = round(random.uniform(20.0, 35.0), 2)  # Random temperature in Celsius
        humidity = round(random.uniform(30.0, 80.0), 2)  # Random humidity percentage

        # Create a point for InfluxDB
        point = (
            Point("jetson_iot")
            .field("temperature", temperature)
            .field("humidity", humidity)
            .field("elapsed_time", elapsed_time)
        )

        # Write to InfluxDB
        try:
            write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
            print(f"Data written to InfluxDB: Temp={temperature}°C, Humidity={humidity}%, Elapsed Time={elapsed_time}s")
        except Exception as e:
            print(f"Error writing data to InfluxDB: {e}")

        # Wait for 10 seconds before generating new data
        time.sleep(10)

# Start the data generation in a separate thread
data_thread = threading.Thread(target=generate_data_periodically, daemon=True)
data_thread.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
