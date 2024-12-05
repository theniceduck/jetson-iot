import os
import cv2
import requests
from ultralytics import YOLO

# Prompt user for ESP32 IP and port
while True:
    esp32_ip = input("Enter the ESP32 IP address (e.g., 192.168.0.131:80): ").strip()
    if ":" in esp32_ip:
        break
    print("Invalid input. Please include the port number (e.g., 192.168.0.131:80).")

# ESP32 endpoint URLs
led_on_url = f"http://{esp32_ip}/ledon"
led_off_url = f"http://{esp32_ip}/ledoff"
buzzer_on_url = f"http://{esp32_ip}/buzzeron"
buzzer_off_url = f"http://{esp32_ip}/buzzeroff"

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# List COCO classes and prompt the user to select one
print("\nAvailable COCO dataset classes:")
for class_id, class_name in model.names.items():
    print(f"{class_id}: {class_name}")

while True:
    try:
        selected_class_id = int(input("\nEnter the class ID you want to track: "))
        if selected_class_id in model.names:
            print(f"Tracking class: {model.names[selected_class_id]}")
            break
        else:
            print("Invalid class ID. Please enter a valid ID from the list above.")
    except ValueError:
        print("Invalid input. Please enter a numerical class ID.")

# Open webcam
cap = cv2.VideoCapture(0)

object_detected = False
detection_cooldown = 5  # Number of consecutive frames for consistent detection
detection_counter = 0  # Counter to track consistent detections

try:
    while cap.isOpened():
        # Read a frame from the webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Run YOLOv8 object detection
        results = model(frame, verbose=False)  # Disable verbose to speed up

        # Check if the selected class is detected
        detected = any([box.cls == selected_class_id for box in results[0].boxes])

        # Update detection logic with cooldown mechanism
        if detected:
            detection_counter += 1
        else:
            detection_counter -= 1

        # Clamp the counter within the cooldown range
        detection_counter = max(0, min(detection_cooldown, detection_counter))

        # Trigger LED ON if the object is consistently detected
        if detection_counter == detection_cooldown and not object_detected:
            print(f"{model.names[selected_class_id]} detected, turning LED ON.")
            requests.get(led_on_url)
            print(f"{model.names[selected_class_id]} detected, turning Buzzer ON.")
            requests.get(buzzer_on_url)
            object_detected = True

        # Trigger LED OFF if the object is consistently not detected
        elif detection_counter == 0 and object_detected:
            print(f"No {model.names[selected_class_id]} detected, turning LED OFF.")
            requests.get(led_off_url)
            print(f"No {model.names[selected_class_id]} detected, turning Buzzer OFF.")
            requests.get(buzzer_off_url)
            object_detected = False

        # Display detections on the frame
        frame = results[0].plot()  # YOLOv8 method to plot detections on the frame

        # Show the frame
        cv2.imshow('YOLOv8 Detection', frame)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected. Exiting gracefully...")
    # Optionally, send an LED OFF signal before exiting
    if object_detected:
        requests.get(led_off_url)
        print("LED turned OFF.")
        requests.get(buzzer_off_url)
        print("Buzzer turned OFF.")

finally:
    # Release the webcam and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    print("Resources released. Goodbye!")
