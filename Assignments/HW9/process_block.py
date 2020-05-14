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
    def __init__(self, _f_v = None, _obj_ht = None, _obj_wt = None):
        self.f_v = _f_v
        self.obj_ht = _obj_ht
        self.obj_wt = _obj_wt
    
    def calc_z_dist(self, v_pix):
        z_dist = (self.f_v*self.obj_ht)/v_pix
        return z_dist
    
    def calc_h_offset(self, v_pix, c_pix):
        z_dist = self.calc_z_dist(v_pix)
        h_dist = (z_dist*c_pix)/self.f_v 
        return h_dist
        
    def calc_angle(self, v_pix, c_pix):
        h_dist = self.calc_h_offset(v_pix, c_pix)
        z_dist = self.calc_z_dist(v_pix)
        angle = math.degrees(math.atan(abs(h_dist)/z_dist))
        if h_dist > 0 :
            angle = -angle
        return angle
    
    def get_f(self, camera:RasPiCamera):
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
                z_dist = self.calc_z_dist(v_pix)
                print(f'z - axis distance calculated : {z_dist} (cm)')
            # Test Angle
            if k == ord('a'):
                print("Angle Testing")
                print(img.shape)
                c_pix = img.shape[1]/2 - win_pts[0][0]
                print(f"Pixels from center = {c_pix}")
                h_dist = self.calc_h_offset(v_pix, c_pix)
                angle = self.calc_angle(v_pix, c_pix)
                print(f'h_dist = {h_dist} cm')
                print(f'z_dist = {z_dist} cm')
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
    def __init__(self, _calib:block_calibration , color = "red"):
        self.calib = _calib
        if color == "red":
            self.low = np.array([0, 70, 50])
            self.high = np.array([180, 255, 255])
            self.hsv_low = np.array([10, 255, 255])
            self.hsv_high = np.array([170, 70, 50])
        
    def center_hieght(self, frame):
        """
        HSV Thresolding of the Red color in given frame
        """

        img = frame.copy()
        img = cv2.medianBlur(img,5)

        # Covert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Threshold the HSV image to get only Red colors
        mask1 = cv2.inRange(hsv, self.low, self.hsv_low)
        mask2 = cv2.inRange(hsv, self.hsv_high, self.high)
        mask = cv2.bitwise_or(mask1,mask2)
        
        # Morphological Operation - Opening
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        # cv2.imshow("mask", mask)
        # Find contours
        contours = cv2.findContours(mask.copy(),
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if imutils.is_cv2() else contours[1]

        # Finding object parameters
        self.center_obj = None
        self.hieght_pix = None

        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            # Reference : https://stackoverflow.com/questions/22470902/understanding-moments-function-in-opencv
            M = cv2.moments(c)
            self.center_obj = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            self.hieght_pix = None
            if radius > 20:
                cv2.circle(img, 
                            (int(x), int(y)),
                            int(radius),
                            (0, 255, 255),
                            2)
                cv2.circle(img,
                            self.center_obj,
                            5,
                            (0, 0, 255),
                            -1)
                
                x_min = max(int(x) - int(radius) - 10, 0)
                x_max = min(int(x) + int(radius) + 10 , img.shape[1])
                
                y_min = max(int(y) - int(radius) - 10, 0)
                y_max = min(int(y) + int(radius) + 10 , img.shape[0])
                
                img = cv2.rectangle(img,
                                    (x_min, y_min),
                                    (x_max, y_max),
                                    (255, 255, 0),
                                    2)
                
                roi = mask[y_min : y_max, x_min : x_max]
                roi = roi.T
                row_or = np.zeros(roi.shape[1])
                
                for row in roi:
                    row_or = np.logical_or(row_or, row)
                row_or = np.where(row_or == True)[0]
                if row_or.size > 0:
                    self.hieght_pix = abs(row_or[0] - row_or[-1])
                
        return img, self.hieght_pix, self.center_obj
    
    def predict_dist_angle(self, img_shape):
        if self.hieght_pix != None:
            c_pix = img_shape[1]/2 - self.center_obj[0]
            return self.calib.calc_z_dist(self.hieght_pix), \
                   self.calib.calc_angle(self.hieght_pix, c_pix)
        else:
            return None, None
    