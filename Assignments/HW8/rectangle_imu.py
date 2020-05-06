import RPi.GPIO as gpio
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('../../utils')

from encoder_class import encoder_class
from motor_driver_class import motor_driver
from imu_thread_class import imu_thread

motor = motor_driver()
motor.init_pwm_mode()
print("motors set to pwm opereation")

encoder = encoder_class()
print("encoder inititalized")

imu = imu_thread()
imu.start_read()
print("IMU inititalized and started to read")

plt_data =[ [0, 650, 650, 0  , 0],[0, 0  , 650, 650, 0]]
color = ['b', 'g', 'r', 'm']

for i, val in enumerate([ [50,23] , [50, 27] , [50, 27] , [50,27]]):
    try:
        encoder.init_callback(motor.set_dutycycle,
                              [[None, None, 0, 0]],
                              motor.set_dutycycle,
                              [[0, 0, None, None]])

        motor.pwm_drive("forward", 75)
        encoder.countRL_till(val[0], val[0])
        motor.pwm_gameover()

        time.sleep(0.5)

        turn_angle = 90
        init_angle = imu.get_orientation()[0]

        if (init_angle + turn_angle) >= 0 :
            final_angle  = int((init_angle + turn_angle)%360)
        else:
            final_angle  = 360 - abs((init_angle + turn_angle))
        
        if turn_angle >= 0:
            command = "pivotright"
        else:
            command = "pivotleft"
        
        motor.pwm_drive(command, 80)
        
        prev_angle = imu.get_orientation()[0]
        zero_crossed = False
        while 1:
            angle = imu.get_orientation()[0]
            print(f'Inital angle = {init_angle} -- Final Angle =  {final_angle} -- Current angle = {angle}')
            
            if abs(prev_angle - angle) > 90 and not zero_crossed:
                zero_crossed = True
             
            if turn_angle >= 0:
                if (final_angle >= init_angle):
                    if angle >= final_angle:
                        break
                elif (final_angle < init_angle):
                    if angle >= final_angle and zero_crossed:
                        break
        
        motor.pwm_gameover()
        
        time.sleep(0.5)
        
        plt.scatter(plt_data[0][i],
        plt_data[1][i], c = color[i])
        plt.plot(plt_data[0][i:i+2],
        plt_data[1][i:i+2], c = color[i])
        
    except KeyboardInterrupt:
        motor.pwm_drive("stop")
        break

time.sleep(0.5)
    
plt.show()

motor.cleanup()
encoder.cleanup()
imu.cleanup()