import RPi.GPIO as gpio
import time
import cv2


import sys
sys.path.append('../../utils')

from servo_class import servo_class
from video_recorder import RasPiCamera

cam = RasPiCamera()
s = servo_class()

def setduty(i, cam, s):
    txt = f"duty cycle : {i/2:0.2f} %"
    print(txt)
    s.set_dutycycle(i/2)
    time.sleep(1)
    image = cam.capture()
    cv2.putText(image,
                txt,
                (30, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("Frame", image)
    cam.video_write(image)
    key = cv2.waitKey(1) & 0xFF

for i in range(10, 20):
    setduty(i, cam, s)    
for i in range(20, 9, -1):
    setduty(i, cam, s)
    
s.cleanup()
cam.cleanup()


