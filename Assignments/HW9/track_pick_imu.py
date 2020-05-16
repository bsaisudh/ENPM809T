import cv2

from process_block import process_block
from process_block import block_calibration
import RPi.GPIO as gpio
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('../../utils')
sys.path.append('../..//Assignments/HW8')

from video_recorder import RasPiCamera
from encoder_class import encoder_class
from motor_driver_class import motor_driver
from imu_thread_class import imu_thread
from servo_class import servo_class
from pid_controller_class import pid_controller, controller_util

from turn_imu_pid import turn_right_util

focal_length = 514.2857142857143
obj_hieght = 7
obj_width = 4.1

servo = servo_class()
camera = RasPiCamera()
calib = block_calibration(focal_length, obj_hieght, obj_width)
block = process_block(calib)
img = camera.capture()

motor = motor_driver()
motor.init_pwm_mode()
print("motors set to pwm opereation")

encoder = encoder_class()
print("encoder inititalized")

imu = imu_thread()
imu.start_read()
print("IMU inititalized and started to read")

util_rt_turn = turn_right_util(motor, imu)
pid_rt = pid_controller(util_rt_turn, 0.5, 0.05, 0.00001)

def move_forward(distance):
    distance = min(distance, 20)
    tics = int(distance/1.0205)
    encoder.init_callback(motor.set_dutycycle,
                              [[None, None, 0, 0]],
                              motor.set_dutycycle,
                              [[0, 0, None, None]])

    motor.pwm_drive("forward", 75)
    
    encoder.countRL_till(tics, tics)
    motor.pwm_gameover()
    
def move_reverse(distance):
    distance = min(distance, 20)
    tics = int(distance/1.0205)
    encoder.init_callback(motor.set_dutycycle,
                              [[None, None, 0, 0]],
                              motor.set_dutycycle,
                              [[0, 0, None, None]])

    motor.pwm_drive("reverse", 75)
    
    encoder.countRL_till(tics, tics)
    motor.pwm_gameover()
    
def turn_imu_pid(turn_angle):
    turn_angle = turn_angle/2
    init_angle = imu.get_orientation()[0]

    if (init_angle + turn_angle) >= 0 :
        final_angle  = int((init_angle + turn_angle)%360)
    else:
        final_angle  = 360 - abs((init_angle + turn_angle))
        
    angle = imu.get_orientation()[0]
    print(f'Move angle = {turn_angle} -- Inital angle = {init_angle} -- Final Angle =  {final_angle} -- Current angle = {angle}')
    
    util_rt_turn.set_sp(final_angle)
    pid_rt.controller(1.5)
    motor.pwm_gameover()
    
def turn_imu(turn_angle):
    init_angle = imu.get_orientation()[0]

    if (init_angle + turn_angle) >= 0 :
        final_angle  = int((init_angle + turn_angle)%360)
    else:
        final_angle  = 360 - abs((init_angle + turn_angle))
    
    if turn_angle >= 0:
        command = "pivotright"
    else:
        command = "pivotleft"
    
    motor.pwm_drive(command, 70)
    
    angle = imu.get_orientation()[0]
    print(f'Move angle = {turn_angle} -- Inital angle = {init_angle} -- Final Angle =  {final_angle} -- Current angle = {angle}')
    
    prev_angle = imu.get_orientation()[0]
    zero_crossed = False
    while 1:
        angle = imu.get_orientation()[0]
        # print(f'Inital angle = {init_angle} -- Final Angle =  {final_angle} -- Current angle = {angle}')
        
        if turn_angle > 0:
            if angle > final_angle:
                break
        else:
            if angle < final_angle:
                break
    motor.pwm_gameover()
        
def servo_grab():
    servo.set_dutycycle(9)
    time.sleep(1)
    move_forward(14)
    time.sleep(1)
    servo.set_dutycycle(6)
    time.sleep(1)
    move_reverse(13)
    time.sleep(1)

def servo_drop():
    turn_imu_pid(90)
    move_forward(20)
    move_forward(20)
    move_forward(20)
    move_forward(20)
    servo.set_dutycycle(9)
    time.sleep(2)
    move_reverse(20)
    time.sleep(1)
    servo.set_dutycycle(5)
    time.sleep(1)
    move_reverse(13)

while 1:
    try:
        img, hieght, center= block.center_hieght(camera.capture())
        dist, angle = block.predict_dist_angle(img.shape)
        if hieght is not None :
            cv2.putText(img,
                        f'{dist:0.2f} cm @ {angle:0.2f} deg',
                        (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(img,
                        f'Object Not Found',
                        (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("thres", img)
        k = cv2.waitKey(10) & 0xFF
        if k == ord('q'):
            break
        time.sleep(0.5)
        if hieght is not None :
            print("-------------")
            print(f'Distance = {dist}, Angle = {angle}')
            if not(angle < 6.34 and angle > 0.34):
                turn_imu_pid(angle-3.34)
                time.sleep(1)
            if dist > 24:
                move_forward(dist-24)
                time.sleep(1)
                continue
            if (angle < 6.34 and angle > 0.34) and (dist < 25):
                servo_grab()
                time.sleep(1)
                servo_drop()
                break
    except KeyboardInterrupt:
        motor.pwm_drive("stop")
        break

motor.cleanup()
encoder.cleanup()
imu.cleanup()
servo.cleanup()

cv2.destroyWindow('thres')
cv2.destroyAllWindows()
camera.cleanup()

