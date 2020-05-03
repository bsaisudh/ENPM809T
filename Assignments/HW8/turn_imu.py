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

init_angle = imu.get_orientation()
motor.pwm_drive("pivotright", 50)
while 1:
    angle = imu.get_orientation()
    print(f'init angle = {init_angle[0]} :: angle = {angle[0]}')
    if(angle[0]-init_angle[0] > 90):
        break
motor.pwm_drive("stop")

motor.cleanup()
encoder.cleanup()
imu.cleanup()