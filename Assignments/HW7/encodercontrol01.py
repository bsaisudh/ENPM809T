import RPi.GPIO as gpio
import time
import cv2

import sys
sys.path.append('../../utils')

from encoder_class import encoder_class

encoder = encoder_class()
print("Turn right wheel")
encoder.count_till(20, encoder.read_right)
encoder.cleanup()
