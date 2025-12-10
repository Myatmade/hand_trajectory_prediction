# Myat Ma De May Phuu Ngon
# 26002304901

# This was used to generate 4 markers at the corners.

import cv2
import cv2.aruco as aruco
import os

# Output folder
output_dir = "aruco_markers_40x30cm"
# Create folder if it doesn't already exist
os.makedirs(output_dir, exist_ok=True)

# Load predefined ArUco dictionary (4x4 grid with 50 possible IDs)
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

# Generate 4 markers (IDs 0 to 3)
for marker_id in range(4):
    # Draw marker with size 500x500 pixels
    marker_img = aruco.drawMarker(aruco_dict, marker_id, 500)  # 500px = ~5cm at 200 DPI
    # Construct file name and save image
    filename = f"{output_dir}/marker_{marker_id}.png"
    cv2.imwrite(filename, marker_img)

print("Markers saved in folder:", output_dir)
