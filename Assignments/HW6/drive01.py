import RPi.GPIO as gpio
import time
import cv2


import sys
sys.path.append('../../utils')

from servo_class import servo_class
from video_recorder import RasPiCamera
from motor_driver_class import motor_driver
from sonar_class import sonar_class

def overlay(image, cmd, dc, dist):
    txt = f"Command : {cmd}"
    cv2.putText(image,
            txt,
            (30, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 255, 0), 2, cv2.LINE_AA)
    txt = f"Duty Cycle : {dc} %"
    cv2.putText(image,
            txt,
            (30, 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 255, 0), 2, cv2.LINE_AA)
    txt = f"Distance : {dist:.2f} cm"
    cv2.putText(image,
            txt,
            (30, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, (0, 255, 0), 2, cv2.LINE_AA)
    return image

camera = RasPiCamera()
servo = servo_class()
motor = motor_driver()
sonar = sonar_class()

key_press = None

while True:
    command = "None"
    dc = "None"
    distance = 0
    if key_press == None:
        key_press = input("Select driving mode: ")
    else:
        print(f"Pressed Key: {key_press} ")            
    if key_press == 'q':
        break
    if key_press == "w" or \
       key_press == "a" or \
       key_press == "s" or \
       key_press == "d":
        command = "motor operation: " + key_press
        motor.key_input(key_press, 0.5)
    if key_press == "p":
        command = "servo control"
        dc = float(input("Duty Cycle: "))
        if dc == 0 :
            print("release load")
            servo.release_load()
        elif dc > 0 :
            servo.set_dutycycle(dc)
    distance = sonar.measure_dist_avg(20, False)
    print("--> Distance = {} cm".format(distance))
    image = camera.capture()
    image = overlay(image, command, dc, distance)
    cv2.imshow("Frame", image)
    key = cv2.waitKey(0) & 0xFF
    camera.video_write(image)
    if key == ord("q"):
        break
    else:
        key_press = chr(key)
    
    
camera.cleanup()
servo.cleanup()
motor.cleanup()
sonar.cleanup()