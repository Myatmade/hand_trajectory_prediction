# Myat Ma De May Phuu Ngon
# 26002304901

# This was used to collect data. There are 9 points and 15 sequences per point.
# After all data is collected, saved in csv. First csv is "hand_trajectory_labeled_15p.csv" and
# another csv after recollection is "hand_trajectory_labeled_new.csv".

import cv2
import mediapipe as mp
import pyrealsense2 as rs
import numpy as np
import csv
import time

# ─────────────── Setup ───────────────
point_labels = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8", "P9"]   # 9 points
current_label_index = 0                                 # Start from the first point
current_label = point_labels[current_label_index]
sequence_id = 0                                         # Sequence ID per point
recording = False                                       # Flag for whether to record

print(f"Start with {current_label}. Press 'n' to start a new sequence. Press 'a' to switch point.")

# ─────────────── CSV ───────────────
# Create CSV file and write header row
csv_file = open("hand_trajectory_labeled_new.csv", mode='w', newline='')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["timestamp", "x_px", "y_px", "z_mm", "point_id", "sequence_id"])

# ─────────────── RealSense ───────────────
# Initilaize RealSense pipeline and enable color and depth streams
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# Align depth to color stream
align = rs.align(rs.stream.color)

# ─────────────── MediaPipe ───────────────
# Initilaize MediaPipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# ─────────────── Loop ───────────────
try:
    while True:
        # Get and align frames
        frames = pipeline.wait_for_frames()
        aligned = align.process(frames)
        depth_frame = aligned.get_depth_frame()
        color_frame = aligned.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # Convert color frame to RGB for MediaPipe
        color_image = np.asanyarray(color_frame.get_data())
        frame_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)

        # Run hand landmark detection
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks on the color image
                mp_drawing.draw_landmarks(color_image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Get index finger tip coordinates
                h, w, _ = color_image.shape
                landmark = hand_landmarks.landmark[8] #index finger
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cx, cy = np.clip(cx, 0, w - 1), np.clip(cy, 0, h - 1)

                # Get depth in mm at fingertip
                z = depth_frame.get_distance(cx, cy) * 1000  # in mm
                ts = time.time()

                # Record if recording is enabled and depth is valid
                if recording and z > 0:
                    csv_writer.writerow([ts, cx, cy, round(z, 2), current_label, sequence_id])

                # Draw indicators
                cv2.circle(color_image, (cx, cy), 8, (0, 255, 0), -1)
                cv2.putText(color_image, f"{round(z, 1)} mm", (cx + 10, cy - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
                cv2.putText(color_image, f"Label: {current_label} | Seq: {sequence_id} | {'REC' if recording else 'IDLE'}",
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 128, 255), 2)

        # Display frame
        cv2.imshow("Tracking + Depth", color_image)
        key = cv2.waitKey(1) & 0xFF

        # Keyboard controls
        
        # quit
        if key == ord('q'):
            break

        # switch to next label
        elif key == ord('s'):
            sequence_id = 0
            recording = False
            current_label_index += 1 
            
            if current_label_index < len(point_labels):
                current_label = point_labels[current_label_index]
                print(f"Switched to: {current_label}")
            else:
                print("All labels completed.")
                break
        # Start new sequence
        elif key == ord('a'):
            sequence_id += 1
            recording = True
            print(f"Started sequence {sequence_id} for {current_label}")

except KeyboardInterrupt:
    print("Interrupted by user")

finally:
    # Cleanup
    print("Saving and exiting")
    csv_file.close()
    pipeline.stop()
    cv2.destroyAllWindows()
