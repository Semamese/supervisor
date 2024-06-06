import cv2
import os


def extract_frames(video_path, output_folder, frame_rate=1):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get video properties
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_fps = cap.get(cv2.CAP_PROP_FPS)

    frame_interval = int(video_fps / frame_rate)
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            frame_filename = os.path.join(output_folder, f"frame_{frame_count:05d}.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"Extracted {frame_filename}")

        frame_count += 1

    cap.release()
    print(f"Finished extracting frames from {video_path}")


# Example usage
video_path = 'C:\project\OKtest.mp4'
output_folder = 'C:\project\Outputimg'
extract_frames(video_path, output_folder, frame_rate=1)
