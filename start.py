import cv2
import numpy as np
from twilio.rest import Client
import shutil
import time
from twilio.twiml.messaging_response import MessagingResponse

# Paths to YOLO configuration, weights, and classes files
yolo_cfg = 'yolo_files/yolov4.cfg'  # Path to YOLO configuration file
yolo_weights = 'yolo_files/yolov4.weights'  # Path to YOLO weights file
coco_names = 'yolo_files/coco.names'  # Path to the class labels (e.g., coco.names)

# Load class labels
with open(coco_names, 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

# Load YOLO model
net = cv2.dnn.readNet(yolo_weights, yolo_cfg)

# Get the output layer names
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Initialize the webcam
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam
if not cap.isOpened():
    print("Error: Unable to access the webcam.")
    exit()

print("Press 'q' to exit the live detection.")

# Flag to track if a screenshot has been taken
screenshot_taken = False
Whatsapp_flag = False
user_response = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture frame.")
        break

    # Get frame dimensions
    height, width, _ = frame.shape

    # Prepare the frame for YOLO (blob from image)
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # Perform a forward pass to get the output
    outs = net.forward(output_layers)

    # Lists for detected bounding boxes, confidences, and class IDs
    boxes = []
    confidences = []
    class_ids = []

    # Process the detections
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.25:  # Confidence threshold
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                # Append to the lists
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maximum Suppression to reduce overlapping boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Check if any indices are returned
    if len(indices) > 0:
        for i in indices.flatten():
            box = boxes[i]
            x, y, w, h = box
            label = f"{class_names[class_ids[i]]}: {confidences[i]:.2f}"
            color = (0, 255, 0)  # Default color (green)

            # Check if the detected object is a person
            if class_names[class_ids[i]].lower() == "person":
                print("SUSPICIOUS")  # Print DANGER if a person is detected
                color = (0, 0, 255)  # Change bounding box color to red

                # Take a screenshot if not already taken
                if not screenshot_taken:
                    screenshot_taken = True  # Update the flag
                    cv2.imwrite("screenshot.jpg", frame)
                    print("Screenshot saved as 'screenshot.jpg'.")
                    destination_folder = "C:/xampp/htdocs/"
                    destination_path = destination_folder + "screenshot.jpg"
                    try:
                        shutil.move("screenshot.jpg", destination_path)
                        print(f"Screenshot moved to {destination_path}.")
                    except Exception as e:
                        print(f"Error moving file: {e}")
                if not Whatsapp_flag:
                    Whatsapp_flag = True
                    account_sid = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                    auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                    from_='whatsapp:+14155238886',
                    to='whatsapp:+919951280286',
                    body= 'Oops! Looks like an INTRUDER!!!!!!!',
                    media_url='https://e288-2409-40f0-104d-c074-d2-800-156-59b9.ngrok-free.app/screenshot.jpg'
                    )
                    time.sleep(5)
                    message2 = client.messages.create(
                    from_='whatsapp:+14155238886',
                    to='whatsapp:+919951280286',
                    body= "We detected the above person roaming around your territory, If the person is suspicious Please Let us know If we should Implement the EMERGENCY ACT!!! Please type your answer.. \nReply with:\nYes\nNo" 
                    )

                    print(message.sid)
                    """while user_response is None:
                        try:
                            last_message = client.messages.list(to='whatsapp:+919951280286', limit=1)
                            if last_message:
                                text = last_message[0].body.strip().lower()
                                if text in ['yes', 'no']:
                                    user_response = text.capitalize()
                                    print(f"User response: {user_response}")
                        except Exception as e:
                            print(f"Error fetching user response: {e}")
                        time.sleep(2)"""
                    while True:
                        last_message = client.messages.list(to='whatsapp:+919951280286', limit=1)
                        text = last_message[0].body.strip().lower()
                        #print("IN THE LOOP")
                        #print(text[10:13])
                        if text[10:13]=='yes':
                            user_response = 'yes'
                            break
                        if text[10:12]=='no':
                            user_response = 'no'
                            break
                        time.sleep(2)
                    print("USER RESPONSE = ",user_response)
                    if user_response=='yes':
                        with open('Emergency_act.py') as f:
                            exec(f.read())

            # Draw the bounding box and label
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Display the frame
    cv2.imshow("Live Object Detection", frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()



