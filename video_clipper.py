import cv2
import os
import logging

logging.basicConfig(format='\033[91m%(levelname)s: %(message)s\033[0m', level=logging.ERROR)

def split_video_segment(video_path, start_time, end_time, output_path="mmaction2/data/table_tennis/train"):
    '''
    Clip the vidoes and save them
    '''
    # Open video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / fps

    # Validate timestamps
    if start_time < 0 or end_time > duration or start_time >= end_time:
        logging.error("Invalid timestamps. Video duration is {duration:.2f}s.")
        cap.release()
        return

    # Calculate frame range
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Create output directory if needed
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # Setup video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    # Jump to the start frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Write frames in the range
    for frame_num in range(start_frame, end_frame):
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    out.release()
    print(f"Saved clip: {output_path} ({start_time:.2f}s to {end_time:.2f}s)")
