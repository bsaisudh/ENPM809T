import numpy as np
import cv2 as cv
import time

import sys
sys.path.append('../../utils')
from video_recorder import RasPiCamera

camera = RasPiCamera()

img = camera.capture()
img = cv.medianBlur(img,5)

# Convert BGR to HSV
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

uh = 170
us = 70
uv = 50
lh = 10
ls = 255
lv = 255
lower_hsv = np.array([lh,ls,lv])
upper_hsv = np.array([uh,us,uv])

l_h,l_s,l_v = 0, 70, 50
u_h,u_s,u_v = 180, 255, 255
l_hsv = np.array([l_h,l_s,l_v])
u_hsv = np.array([u_h,u_s,u_v])

# Threshold the HSV image to get only Red colors
mask1 = cv.inRange(hsv, l_hsv, lower_hsv)
mask2 = cv.inRange(hsv, upper_hsv, u_hsv)

mask = cv.bitwise_and(mask1,mask2)

window_name = "HSV Calibrator"
cv.namedWindow(window_name)


def nothing(x):
    print("Trackbar value: " + str(x))
    pass

# create trackbars for Upper HSV
cv.createTrackbar('UpperH',window_name,0,255,nothing)
cv.setTrackbarPos('UpperH',window_name, uh)

cv.createTrackbar('UpperS',window_name,0,255,nothing)
cv.setTrackbarPos('UpperS',window_name, us)

cv.createTrackbar('UpperV',window_name,0,255,nothing)
cv.setTrackbarPos('UpperV',window_name, uv)

# create trackbars for Lower HSV
cv.createTrackbar('LowerH',window_name,0,255,nothing)
cv.setTrackbarPos('LowerH',window_name, lh)

cv.createTrackbar('LowerS',window_name,0,255,nothing)
cv.setTrackbarPos('LowerS',window_name, ls)

cv.createTrackbar('LowerV',window_name,0,255,nothing)
cv.setTrackbarPos('LowerV',window_name, lv)

# create trackbars for lowerLimit
cv.createTrackbar('UH',window_name,0,255,nothing)
cv.setTrackbarPos('UH',window_name, u_h)

cv.createTrackbar('US',window_name,0,255,nothing)
cv.setTrackbarPos('US',window_name, u_s)

cv.createTrackbar('UV',window_name,0,255,nothing)
cv.setTrackbarPos('UV',window_name, u_v)

# create trackbars for Lower HSV
cv.createTrackbar('LH',window_name,0,255,nothing)
cv.setTrackbarPos('LH',window_name, l_h)

cv.createTrackbar('LS',window_name,0,255,nothing)
cv.setTrackbarPos('LS',window_name, l_s)

cv.createTrackbar('LV',window_name,0,255,nothing)
cv.setTrackbarPos('LV',window_name, l_v)

font = cv.FONT_HERSHEY_SIMPLEX

while(1):
    img = camera.capture()
    img = cv.medianBlur(img,5)

    # Convert BGR to HSV
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Threshold the HSV image to get only Red colors
    mask1 = cv.inRange(hsv, l_hsv, lower_hsv)
    mask2 = cv.inRange(hsv, upper_hsv, u_hsv)
    mask = cv.bitwise_or(mask1,mask2)
    cv.putText(mask,'L HSV: [' + str(l_h) +',' + str(l_s) + ',' + str(l_v) + ']', (10,30), font, 0.5, (200,255,155), 1, cv.LINE_AA)
    cv.putText(mask,'Lower HSV: [' + str(lh) +',' + str(ls) + ',' + str(lv) + ']', (10,60), font, 0.5, (200,255,155), 1, cv.LINE_AA)
    cv.putText(mask,'U HSV: [' + str(u_h) +',' + str(u_s) + ',' + str(u_v) + ']', (10,90), font, 0.5, (200,255,155), 1, cv.LINE_AA)
    cv.putText(mask,'Upper HSV: [' + str(uh) +',' + str(us) + ',' + str(uv) + ']', (10,120), font, 0.5, (200,255,155), 1, cv.LINE_AA)
    mask = cv.resize(mask, (int(640/2), int(480/2)))
    cv.imshow(window_name,mask)

    k = cv.waitKey(1) & 0xFF
    if k == 27: # esc key
        break
    # get current positions of Upper HSV trackbars
    uh = cv.getTrackbarPos('UpperH',window_name)
    us = cv.getTrackbarPos('UpperS',window_name)
    uv = cv.getTrackbarPos('UpperV',window_name)
    upper_red = np.array([uh,us,uv])
    # get current positions of Lower HSCV trackbars
    lh = cv.getTrackbarPos('LowerH',window_name)
    ls = cv.getTrackbarPos('LowerS',window_name)
    lv = cv.getTrackbarPos('LowerV',window_name)
    
    # get current positions of Upper trackbars
    u_h = cv.getTrackbarPos('UH',window_name)
    u_s = cv.getTrackbarPos('US',window_name)
    u_v = cv.getTrackbarPos('UV',window_name)
    upper_red = np.array([uh,us,uv])
    # get current positions of Lower trackbars
    l_h = cv.getTrackbarPos('LH',window_name)
    l_s = cv.getTrackbarPos('LS',window_name)
    l_v = cv.getTrackbarPos('LV',window_name)
    
    upper_hsv = np.array([uh,us,uv])
    lower_hsv = np.array([lh,ls,lv])
    
    l_hsv = np.array([l_h,l_s,l_v])
    u_hsv = np.array([u_h,u_s,u_v])

    time.sleep(.1)

cv.destroyAllWindows()
camera.cleanup()

