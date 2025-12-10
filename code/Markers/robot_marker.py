# Myat Ma De May Phuu Ngon
# 26002304901

# This code was used to generate two markers for two robots to determine their position

# using IDs 50 and 51 from the DICT_4X4_1000 dictionary which provides 1000 unique markers

import cv2
import cv2.aruco as aruco
import os

# Create output directory if not exists
output_dir = "generated_markers"
os.makedirs(output_dir, exist_ok=True)

# Use a larger dictionary to avoid overlap with existing markers
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_1000)

# IDs to generate
marker_ids = [50, 51]  # Chosen to avoid conflict with table markers

# Generate and save markers
for marker_id in marker_ids:
    marker_img = aruco.generateImageMarker(aruco_dict, marker_id, 700)
    filename = os.path.join(output_dir, f"aruco_marker_{marker_id}.png")
    cv2.imwrite(filename, marker_img)
    print(f"Saved: {filename}")
