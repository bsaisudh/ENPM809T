import time

import sys
sys.path.append('../../utils')

from imu_thread_class import imu_thread
from motor_driver_class import motor_driver

motor = motor_driver()
motor.init_pwm_mode()
print("motors set to pwm opereation")

imu = imu_thread()
imu.start_read()
print("IMU inititalized and started to read")
while 1:
    try:
        turn_angle = int(input("Angle to turn : "))
        init_angle = imu.get_orientation()[0]

        if (init_angle + turn_angle) >= 0 :
            final_angle  = int((init_angle + turn_angle)%360)
        else:
            final_angle  = 360 - abs((init_angle + turn_angle))
        
        if turn_angle >= 0:
            command = "pivotright"
        else:
            command = "pivotleft"
        
        motor.pwm_drive(command, 90)
        
        prev_angle = imu.get_orientation()[0]
        zero_crossed = False
        while 1:
            angle = imu.get_orientation()[0]
            print(f'Inital angle = {init_angle} -- Final Angle =  {final_angle} -- Current angle = {angle}')
            
            if abs(prev_angle - angle) > 90 and not zero_crossed:
                zero_crossed = True
             
            if turn_angle >= 0:
                if (angle >= final_angle):
                    break
                if (final_angle >= init_angle):
                    if angle >= final_angle:
                        break
                elif (final_angle < init_angle):
                    if angle >= final_angle and zero_crossed:
                        break
            else:
                if (angle <= final_angle):
                    break
                if (final_angle <= init_angle):
                    if angle <= final_angle and zero_crossed:
                        break
                elif (final_angle > init_angle):
                    if angle <= final_angle and zero_crossed:
                        break
            #if(angle < final_angle+2 and angle > final_angle-2):
            #    break
        motor.pwm_drive("stop")
    except KeyboardInterrupt:
        motor.pwm_drive("stop")
        break
motor.cleanup()
imu.cleanup()