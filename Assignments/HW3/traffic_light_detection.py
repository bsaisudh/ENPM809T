import cv2
import numpy as np
import imutils


def threshold_hsv_green(frame):
    """
    HSV Thresolding of the Green color in given frame
    """

    image = frame.copy()

    # Covert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Green Color HSV Range
    lower_green = np.array([50, 100, 100])
    upper_green = np.array([90, 255, 255])

    # Thresolding HSV range to get only green mask
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    masked_image =  cv2.bitwise_and(image, image, mask=mask_green)

    mask_hsv_comparision = np.hstack((image, hsv, masked_image))

    # Morphological Operation - Opening
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.dilate(mask_green, None, iterations=2)

    # Find contours
    contours = cv2.findContours(mask_green.copy(),
                                cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]

    # Finding green light
    center = None

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        # Reference : https://stackoverflow.com/questions/22470902/understanding-moments-function-in-opencv
        M = cv2.moments(c)
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))

        if radius > 10:
            cv2.circle(image, 
                        (int(x), int(y)),
                        int(radius),
                        (0, 255, 255),
                        2)
            cv2.circle(image,
                        center,
                        5,
                        (0, 0, 255),
                        -1)

    return image, mask_hsv_comparision
