import RPi.GPIO as gpio
import time
import cv2
import matplotlib.pyplot as plt
import numpy as np

import sys
sys.path.append('../../utils')

from encoder_class import encoder_class
from motor_driver_class import motor_driver

encoder = encoder_class()
print("encoder inititalized")
motor = motor_driver()
motor.init_pwm_mode()
print("motors set to pwm opereation")

motor.pwm_drive("rightreverse", 14)
dataR = []
dataL = []
encoder.countRL_till(20, 0, dataR, dataL)
motor.pwm_gameover()

plt.figure()
plt.subplot(211)
plt.plot(dataR)
plt.title("Right Encoder")

plt.subplot(212)
plt.plot(dataL)
plt.title("Left Encoder")

plt.show()

# np.savetxt("encoder_data_right.txt", dataR)
# np.savetxt("encoder_data_left.txt", dataL)

motor.cleanup()
encoder.cleanup()


