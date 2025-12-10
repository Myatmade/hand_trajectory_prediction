Setup installation

python version used is 3.12.7
Please make sure you can use pip.

For IDE, we installed anaconda and created a virtual environment named "hand".

Please put all of the files from "Results" in the same folder, extract all files and remove their respective folders, including data samples.
The codes were written in a way that expects all files to be in the same folder.

You can unzip the preliminary_test.zip and try out the set up for depth camera, hand tracking and robot position tracking.

(Libraries)
Please make sure you have the necessary libraries installed.

mediapipe
run this in terminal: pip install mediapipe

pyrealsense2 (camera)
Please plug in with the usb port to pc first.
official github: https://github.com/IntelRealSense/librealsense/releases/tag/v2.56.3
run this in terminal: pip install pyrealsense2

cv2
run this in terminal: pip install opencv-python

numpy
run this in terminal: pip install numpy

matplotlib
run this in terminal: pip install matplotlib

pandas
run this in terminal: pip install pandas

seaborn
run this in terminal: pip install seaborn

tensorflow
run this in terminal: pip install tensorflow

scipy
run this in terminal: pip install scipy

fastdtw
run this in terminal: pip install fastdtw

scikit-learn
run this in terminal: pip install scikit-learn

The code for each model has the testing in live mode at the end of the file.
If you want to test the model, you can run the last block in the code without retraining as I have included the saved models in each model folder.

(Physical Setup)
Put markers on the table. Draw grid and make 9 points on paper and put it on table. Setup camera.
You might need to adjust the camera position and angle to get a good view of the markers. However, it is suggested to recollect the data for a new environment.

