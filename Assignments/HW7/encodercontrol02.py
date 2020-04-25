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

motor.pwm_drive("rightforward", 14)
data = []
encoder.count_till(20, encoder.read_right, data)
motor.pwm_gameover()

plt.plot(data)
plt.title("Encoder Reading")
plt.show()
np.savetxt("encoder_data.txt", data)

motor.cleanup()
encoder.cleanup()

