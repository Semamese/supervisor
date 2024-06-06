import cv2


def nothing(x):
    pass


def open_webcam_edge_detection():
    # Open a connection to the webcam (default camera is usually at index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Create a window named 'Edge Detection'
    cv2.namedWindow('Webcam Edge Detection')

    # Create trackbars for lower and upper threshold
    cv2.createTrackbar('Lower Threshold', 'Webcam Edge Detection', 100, 255, nothing)
    cv2.createTrackbar('Upper Threshold', 'Webcam Edge Detection', 200, 255, nothing)

    # Loop to continuously get frames from the webcam
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            print("Failed to grab frame")
            break

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Get current positions of the trackbars
        lower_thresh = cv2.getTrackbarPos('Lower Threshold', 'Webcam Edge Detection')
        upper_thresh = cv2.getTrackbarPos('Upper Threshold', 'Webcam Edge Detection')

        # Apply Canny edge detection with dynamic thresholds
        edges = cv2.Canny(gray_frame, lower_thresh, upper_thresh)

        # Display the resulting frame
        cv2.imshow('Webcam Edge Detection', edges)

        # Press 'q' on the keyboard to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    open_webcam_edge_detection()
