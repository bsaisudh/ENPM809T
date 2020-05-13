import cv2
import numpy as np
import imutils
import time
import math

import sys
sys.path.append('../../utils')
from video_recorder import RasPiCamera

global win_pts

# Mouse Click Event
# https://www.pyimagesearch.com/2015/03/09/capturing-mouse-click-events-with-python-and-opencv/

def onmouse(event, x, y, flags, param):
    global win_pts
    if event == cv2.EVENT_LBUTTONUP:
        print(f"x: {x} , y: {y}")
        if len(win_pts) < 2:
            win_pts.append((x, y))
        else:
            win_pts.pop(0)
            win_pts.append((x,y))

class block_calibration:
    def __init__(self):
        self.f_v = None
        self.obj_ht = None
        self.obj_wt = None
        
    def get_f(self, camera:RasPiCamera, ):
        global win_pts
        print('Entering Calibraion Block')
        win_pts = []
        win_name = 'calibration_block'
        img = camera.capture()
        cv2.imshow(win_name, img)
        cv2.setMouseCallback(win_name, onmouse)
        while 1:
            cv2.imshow(win_name, img)
            k = cv2.waitKey(1) & 0xFF
            # exit
            if k == 27 or k == ord('q'): # esc key
                print("exit")
                break
            # New Image
            if k == ord('n'):
                img = camera.capture()
                win_pts = []
            # cancel selected points
            if k == ord('c'):
                win_pts = []
            # Vertical calibration
            if k == ord('v'):
                print("Vertical Calibration")
                v_pix = abs(win_pts[0][1] - win_pts[1][1])
                print(f"Vertical pixels = {v_pix} ({win_pts[0][1]} - {win_pts[1][1]})")
                print(f"Horizantal pixels = {abs(win_pts[0][0] - win_pts[1][0])}")
                obj_dist = int(input("Enter z-axis distance(cm): "))
                self.obj_ht = int(input("Enter object height(cm): "))
                self.f_v = (obj_dist*v_pix)/self.obj_ht
                print(f'Vertical focal length calculated : {self.f_v} (cm)')
            # Horizontal Calibration
            if k == ord('h'):
                print("Horizantal Calibration")
                h_pix = abs(win_pts[0][0] - win_pts[1][0])
                print(f"Vertical pixels = abs(win_pts[0][1] - win_pts[1][1])")
                print(f"Horizontal pixels = {v_pix}")
                obj_dist = int(input("Enter z-axis distance(cm): "))
                self.obj_wt = int(input("Enter object width(cm): "))
                self.f_h = (obj_dist*h_pix)/self.obj_wt
                print(f'Vertical focal length calculated : {self.f_h} (cm)')
            # Test mode Vertical
            if k == ord("l"):
                print('Test Mode Vertical')
                v_pix = abs(win_pts[0][1] - win_pts[1][1])
                print(f"Vertical pixels = {v_pix}")
                z_dist = (self.f_v*self.obj_ht)/v_pix
                print(f'z - axis distance calculated : {z_dist} (cm)')
            # Test Angle
            if k == ord('a'):
                print("Angle Testing")
                print(img.shape)
                c_pix = img.shape[1]/2 - win_pts[0][0]
                print(f"Pixels from center = {c_pix}")
                h_dist = (z_dist*c_pix)/self.f_v
                angle = math.degrees(math.atan(abs(h_dist)/z_dist))
                if h_dist <= 0 :
                    angle = -angle
                print(f'h_dist = {h_dist} cm')
                print(f'angle = {angle} degrees')
            # Test mode horizontal
            if k == ord("w"):
                print('Test Mode Horizontal')
                h_pix = abs(win_pts[0][0] - win_pts[1][0])
                print(f"Horizontal pixels = {h_pix}")
                z_dist = (self.f_h*self.obj_wt)/h_pix
                print(f'z - axis distance calculated : {z_dist} (cm)')
            # plot points
            for pt in win_pts:
                cv2.circle(img, pt, 4, (255, 255, 0), -1)
                
        cv2.destroyWindow(win_name)

class process_block:
    def __init__(self, color = "red"):
        
        if color == 'red':
            self.low = [0, 70, 50]
            self.high = [180, 255, 255]
            self.hsv_low = [170, 70, 50]
            self.hsv_high = [10, 255, 255]
        
    def threshold_hsv_red(self, frame):
        """
        HSV Thresolding of the Red color in given frame
        """

        image = frame.copy()

        # Covert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Green Color HSV Range
        lower_red = np.array([50, 100, 100])
        upper_red = np.array([90, 255, 255])

        # Thresolding HSV range to get only green mask
        mask_red = cv2.inRange(hsv, lower_red, upper_red)
        masked_image =  cv2.bitwise_and(image, image, mask=mask_red)

        self.mask_hsv_comparision = np.hstack((image, hsv, masked_image))

        # Morphological Operation - Opening
        mask_red = cv2.erode(mask_green, None, iterations=2)
        mask_red = cv2.dilate(mask_green, None, iterations=2)

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

        return image
    
    def get_distance(self):
        pass
    
    def display(self):
        cv2.imshow("mask_hsv_comparison", self.mask_hsv_comparision)
    