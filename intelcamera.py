import os
import sys
import cv2
import pyrealsense2 as rs
import numpy as np
import uuid

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

pipeline.start(config)

def captureFrame(img):
    print("Capturing Image...")
    data_dir = os.path.join(os.getcwd(), 'data')
    if (not os.path.isdir(data_dir)):
        os.mkdir(data_dir)

    img_name = str(uuid.uuid4()) + ".jpg"
    img_dir = os.path.join(data_dir, img_name)

    cv2.imwrite(img_dir, img)
    print("Captured Image " + img_name)

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
<<<<<<< HEAD

        color_image = np.asanyarray(color_frame.get_data())
        cv2.imshow('RealSense', color_image)
=======
        
        color_image = np.asanyarray(color_frame.get_data())
        cv2.imshow('RealSense', color_image)
        
>>>>>>> 6501d6d2c29f046b37c878b06e778f19393cc817
        key = cv2.waitKey(1)
        if (key == 112): # 'p' key
            captureFrame(color_image)
        elif (key == 27): # 'esc' key
            break
finally:
    pipeline.stop()

print("Finished")
