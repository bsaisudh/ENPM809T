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

encoder.init_callback(motor.set_dutycycle,
                      [[None, None, 0, 0]],
                      motor.set_dutycycle,
                      [[0, 0, None, None]])

dataR = []
dataL = []

motor.pwm_drive("forward", 50)
encoder.countRL_till(97, 97, dataR, dataL)
motor.pwm_gameover()

fig = plt.figure()
fig.suptitle("Forward")
plt.subplot(211)
plt.plot(dataR)
plt.ylabel("Right Encoder")

plt.subplot(212)
plt.plot(dataL)
plt.ylabel("Left Encoder")

time.sleep(1)

dataR = []
dataL = []

motor.pwm_drive("reverse", 50)
encoder.countRL_till(97, 97, dataR, dataL)
motor.pwm_gameover()

fig = plt.figure()
fig.suptitle("Reverse")
plt.subplot(211)
plt.plot(dataR)
plt.ylabel("Right Encoder")

plt.subplot(212)
plt.plot(dataL)
plt.ylabel("Left Encoder")

time.sleep(1)

encoder.init_callback(motor.set_dutycycle,
                      [[0, 0, 0, 0]],
                      motor.set_dutycycle,
                      [[None, None, None, None]])

dataR = []
dataL = []

motor.pwm_drive("pivotright", 75)
encoder.countRL_till(30, 0, dataR, dataL)
motor.pwm_gameover()

fig = plt.figure()
fig.suptitle("Pivot Right")
plt.subplot(211)
plt.plot(dataR)
plt.ylabel("Right Encoder")

plt.subplot(212)
plt.plot(dataL)
plt.ylabel("Left Encoder")

time.sleep(1)

dataR = []
dataL = []

motor.pwm_drive("pivotleft", 75)
encoder.countRL_till(30, 0, dataR, dataL)
motor.pwm_gameover()

fig = plt.figure()
fig.suptitle("Pivot Left")
plt.subplot(211)
plt.plot(dataR)
plt.ylabel("Right Encoder")

plt.subplot(212)
plt.plot(dataL)
plt.ylabel("Left Encoder")

plt.show()

motor.cleanup()
encoder.cleanup()




