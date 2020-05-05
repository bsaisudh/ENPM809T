import RPi.GPIO as gpio
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('../../utils')

from encoder_class import encoder_class
from motor_driver_class import motor_driver

motor = motor_driver()
motor.init_pwm_mode()
print("motors set to pwm opereation")

encoder = encoder_class()
print("encoder inititalized")

plt_data =[ [0, 650, 650, 0  , 0],[0, 0  , 650, 650, 0]]
color = ['b', 'g', 'r', 'm']

for i, val in enumerate([ [50,30] , [50, 30] , [50, 25] , [50,25]]):
    encoder.init_callback(motor.set_dutycycle,
                          [[None, None, 0, 0]],
                          motor.set_dutycycle,
                          [[0, 0, None, None]])

    motor.pwm_drive("forward", 75)
    encoder.countRL_till(val[0], val[0])
    motor.pwm_gameover()

    time.sleep(0.5)

    encoder.init_callback(motor.set_dutycycle,
                          [[0, 0, 0, 0]],
                          motor.set_dutycycle,
                          [[None, None, None, None]])

    motor.pwm_drive("pivotright", 80)
    encoder.countRL_till(val[1], 0)
    motor.pwm_gameover()

    plt.scatter(plt_data[0][i],
                plt_data[1][i], c = color[i])
    plt.plot(plt_data[0][i:i+2],
             plt_data[1][i:i+2], c = color[i])

time.sleep(0.5)
    
plt.show()

motor.cleanup()
encoder.cleanup()