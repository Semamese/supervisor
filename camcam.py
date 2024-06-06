import cv2
import numpy as np

def open_webcam_hand_detection():
    # Open a connection to the webcam (default camera is usually at index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Convert the frame to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define range for skin color in HSV
        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)

        # Threshold the HSV image to get only skin colors
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # Apply some morphological operations to remove noise
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.erode(mask, kernel, iterations=2)
        mask = cv2.GaussianBlur(mask, (5, 5), 100)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour (which should be the hand)
        if contours:
            cnt = max(contours, key=cv2.contourArea)
            # Draw the contour on the frame
            cv2.drawContours(frame, [cnt], -1, (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Webcam Hand Detection', frame)

        # Press 'q' on the keyboard to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    open_webcam_hand_detection()
