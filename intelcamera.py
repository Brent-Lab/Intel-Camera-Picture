import os
import sys
import numpy as np
import uuid
from functools import reduce

import cv2
import pyrealsense2 as rs
from realsense_device_manager import DeviceManager

CAMERA_RESOLUTION_WIDTH = 1920#1280
CAMERA_RESOLUTION_HEIGHT = 1080#720
CAMERA_FRAME_RATE = 30

DATA_FOLDER_NAME = 'data'

CV_WINDOW_NAME = 'RealSense'
INIT_WINDOW_WIDTH = 700
INIT_WINDOW_HEIGHT = 700

def captureFrame(img):
    data_dir = os.path.join(os.getcwd(), DATA_FOLDER_NAME)
    if (not os.path.isdir(data_dir)):
        os.mkdir(data_dir)

    img_name = str(uuid.uuid4()) + ".jpg"
    img_dir = os.path.join(data_dir, img_name)

    return cv2.imwrite(img_dir, img), img_dir

def run():
    rs_config = rs.config()
    rs_config.enable_stream(rs.stream.color, CAMERA_RESOLUTION_WIDTH, CAMERA_RESOLUTION_HEIGHT, rs.format.bgr8, CAMERA_FRAME_RATE)

	# Use the device manager class to enable the devices and get the frames
    device_manager = DeviceManager(rs.context(), rs_config)
    device_manager.enable_all_devices()

    assert (len(device_manager._available_devices) > 0)
    
    try:
        while True:
            frames = device_manager.poll_frames()

            color_images = []
            for key in frames.keys():
                color_frame = frames[key][rs.stream.color].get_data()
                color_image = np.asanyarray(color_frame)
                color_images.append(color_image)

            if len(color_images) == 0:
                continue

            images = np.vstack(color_images)

            cv2.namedWindow(CV_WINDOW_NAME, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(CV_WINDOW_NAME, INIT_WINDOW_WIDTH, INIT_WINDOW_HEIGHT)
            cv2.imshow(CV_WINDOW_NAME, images)

            k = cv2.waitKey(1)
            if k == 112: # 'p' key
                print("Capturing images...")
                for color_image in color_images:
                    status, dir = captureFrame(color_image)
                    if status: print("Saved image to " + dir)
                    else: print("A problem occurred when capturing the frame.")
            elif k == 27:
                break
    except KeyboardInterrupt:
        print("The program was interupted by the user. Closing the program...")
    finally:
        device_manager.disable_streams()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run()
