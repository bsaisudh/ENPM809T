import RPi.GPIO as gpio
import time
import numpy as np

class encoder_class:
    def __init__(self):
        self.init_counter()
        self.init()
        
    def init(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(12, gpio.IN, pull_up_down = gpio.PUD_UP)
    
    def cleanup(self):
        gpio.cleanup()
        
    def read_right(self):
        return gpio.input(12)
    
    def init_counter(self):
        self.counter = np.uint(0)
    
    def count_till(self, count):
        button = int(0)
        while True:
            right = self.read_right()
            if(int(right) != button):
                button = right
                self.counter += 1
                print(f"Counter Value : {self.counter}")
            if self.counter > count:
                print ("--- Thanks for playing the game ---")
                break
    
if __name__ == "__main__":
    
    import sys
    sys.path.append('../../utils')
    
    from motor_driver_class import motor_driver
    
    motor = motor_driver()
    encoder = encoder_class()
    encoder.init_counter()
    
    encoder.count_till(30)
    encoder.cleanup()