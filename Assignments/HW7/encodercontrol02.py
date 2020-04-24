import RPi.GPIO as gpio
import time
import cv2

import sys
sys.path.append('../../utils')

from encoder_class import encoder_class
from motor_driver_class import motor_driver

encoder = encoder_class()
print("encoder inititalized")
motor = motor_driver()
motor.init_pwm_mode()
print("motors set to pwm opereation")

motor.pwm_drive("pivotright", 14)
encoder.count_till(20, encoder.read_right)
motor.pwm_gameover()

motor.cleanup()
encoder.cleanup()

