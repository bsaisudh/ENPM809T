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
encoder.init_callback(motor.set_dutycycle,
                      [[0, 0, 0, 0]],
                      motor.set_dutycycle,
                      [[None, None, None, None]])
print("encoder inititalized")

tics = int(input("enter number of tics: "))
dc = int(input("enter pwm duty cycle: "))

for i in range(4):
    motor.pwm_drive("pivotright", dc)
    dataR = []
    dataL = []
    encoder.countRL_till(tics, 0, dataR, dataL)
    motor.pwm_gameover()
    time.sleep(0.5)
    
plt.figure()
plt.subplot(211)
plt.plot(dataR)
plt.ylabel("Right Encoder")

plt.subplot(212)
plt.plot(dataL)
plt.ylabel("Left Encoder")

plt.show()

# np.savetxt("encoder_data_right.txt", dataR)
# np.savetxt("encoder_data_left.txt", dataL)

motor.cleanup()
encoder.cleanup()



