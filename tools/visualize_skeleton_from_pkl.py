import pickle
import cv2
import numpy as np
import os
import argparse

# COCO skeleton pairs
SKELETON = [
    (5, 7), (7, 9),
    (6, 8), (8, 10),
    (5, 6),
    (5, 11), (6, 12),
    (11, 12), (11, 13),
    (13, 15), (12, 14),
    (14, 16)
]

def draw_skeleton(frame, kpts):
    for i, j in SKELETON:
        x1, y1 = kpts[i]
        x2, y2 = kpts[j]

        # Check for valid coordinates (assuming 0 is invalid/missing)
        if x1 > 0 and y1 > 0 and x2 > 0 and y2 > 0:
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

    for (x, y) in kpts:
        if x > 0 and y > 0:
            cv2.circle(frame, (int(x), int(y)), 4, (0, 0, 255), -1)

    return frame


def visualize_skeleton_only(pkl_path, video_path, output="skeleton_only.mp4", person_id=0):

    print("Loading:", pkl_path)
    with open(pkl_path, "rb") as f:
        data = pickle.load(f)

    kpts = np.array(data["keypoint"])   # (persons, frames, 17, 2)
    kpts = kpts.transpose(1, 0, 2, 3)   # -> (frames, persons, 17, 2)

    total_frames = kpts.shape[0]

    # Load video to get dimensions and FPS
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("ERROR opening video:", video_path)
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"Video FPS={fps}, size=({W},{H})")

    out = cv2.VideoWriter(
        output,
        cv2.VideoWriter_fourcc(*'mp4v'),
        fps,
        (W, H)
    )

    frame_idx = 0

    while True:
        ret, _ = cap.read() # Read the frame to advance the video, but ignore the image data
        
        if not ret or frame_idx >= total_frames:
            break

        # Create a black background instead of using the video frame
        # (Height, Width, 3 color channels)
        black_frame = np.zeros((H, W, 3), dtype=np.uint8)

        keypoints = kpts[frame_idx][person_id]

        # Draw skeleton onto the black frame
        frame = draw_skeleton(black_frame, keypoints)

        out.write(frame)

        frame_idx += 1

    cap.release()
    out.release()
    print("Saved:", output)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate skeleton animation (black background)")
    parser.add_argument("--pickle", type=str, required=True, help="Path to pickle file containing keypoints")
    parser.add_argument("--video", type=str, required=True, help="Path to original video (for dims/fps)")
    parser.add_argument("--output", type=str, default="skeleton_only.mp4", help="Output video path")
    parser.add_argument("--person", type=int, default=0, help="Person ID to draw")
    args = parser.parse_args()

    visualize_skeleton_only(
        pkl_path=args.pickle,
        video_path=args.video,
        output=args.output,
        person_id=args.person
    )