import cv2
import numpy as np


def hsv_thresolding_green(frame):
    """
    HSV Thresolding of the Green color in given frame
    """

    # Covert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Green Color HSV Range
    lower_green = np.array([50, 100, 100])
    upper_green = np.array([90, 255, 255])

    # Thresolding HSV range to get only green mask
    mask_green = cv2.inRange(hsv, lower_green, upper_green)

    return mask_green