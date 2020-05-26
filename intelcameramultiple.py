import os
import sys
import cv2
import numpy as np
import uuid

def captureFrame(img):
    print("Capturing Image...")
    data_dir = os.path.join(os.getcwd(), 'data')
    if (not os.path.isdir(data_dir)):
        os.mkdir(data_dir)

    img_name = str(uuid.uuid4()) + ".jpg"
    img_dir = os.path.join(data_dir, img_name)

    cv2.imwrite(img_dir, img)
    print("Captured Image " + img_name)

cam = cv2.VideoCapture("/dev/video0")
#cam2 = cv2.VideoCapture(0)

cv2.namedWindow("Cameras")
while True:
    ret, frame = cam.read()
#    ret2, frame2 = cam2.read()
    if not ret:
        continue

#    combined_frame = np.hstack(frame, frame2)

    cv2.imshow("Cameras", frame)
    k = cv2.waitKey(1)
    if k == 27:
        break
