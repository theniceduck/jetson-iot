import os
import cv2
import requests
from ultralytics import YOLO

# ESP32 IP and endpoint
esp32_ip = "http://191.168.0.131"  # Use environment variable for ESP32's IP address
led_on_url = f"{esp32_ip}/ledon"
led_off_url = f"{esp32_ip}/ledoff"
buzzer_on_url = f"{esp32_ip}/buzzeron"
buzzer_off_url = f"{esp32_ip}/buzzeroff"

# Load YOLOv8 model
model = YOLO('yolov8n.pt')

# Specify the class ID to track (e.g., 0 for 'person')
selected_class_id = 39  # Change this to track a different class
print(f"Tracking class: {model.names[selected_class_id]}")

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

"""
# Classes
names:
  0: person
  1: bicycle
  2: car
  3: motorcycle
  4: airplane
  5: bus
  6: train
  7: truck
  8: boat
  9: traffic light
  10: fire hydrant
  11: stop sign
  12: parking meter
  13: bench
  14: bird
  15: cat
  16: dog
  17: horse
  18: sheep
  19: cow
  20: elephant
  21: bear
  22: zebra
  23: giraffe
  24: backpack
  25: umbrella
  26: handbag
  27: tie
  28: suitcase
  29: frisbee
  30: skis
  31: snowboard
  32: sports ball
  33: kite
  34: baseball bat
  35: baseball glove
  36: skateboard
  37: surfboard
  38: tennis racket
  39: bottle
  40: wine glass
  41: cup
  42: fork
  43: knife
  44: spoon
  45: bowl
  46: banana
  47: apple
  48: sandwich
  49: orange
  50: broccoli
  51: carrot
  52: hot dog
  53: pizza
  54: donut
  55: cake
  56: chair
  57: couch
  58: potted plant
  59: bed
  60: dining table
  61: toilet
  62: tv
  63: laptop
  64: mouse
  65: remote
  66: keyboard
  67: cell phone
  68: microwave
  69: oven
  70: toaster
  71: sink
  72: refrigerator
  73: book
  74: clock
  75: vase
  76: scissors
  77: teddy bear
  78: hair drier
  79: toothbrush
  
"""