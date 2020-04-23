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
        gpio.setup(7, gpio.IN, pull_up_down = gpio.PUD_UP)
    
    def cleanup(self):
        gpio.cleanup()
        
    def read_right(self):
        return gpio.input(12)
    
    def read_left(self):
        return gpio.input(7)
    
    def init_counter(self):
        self.counter = np.uint(0)
    
    def count_till(self, count, read_fntn):
        button = int(0)
        while True:
            reading = read_fntn()
            if(int(reading) != button):
                button = reading
                self.counter += 1
                print(f"Counter Value : {self.counter}")
            if self.counter > count:
                print ("--- Thanks for playing the game ---")
                break
    
if __name__ == "__main__":
    
    run_motor = int(input("Run with motor?(0: no ; >0:yes) : "))
    
    if (run_motor > 0): 
        import sys
        sys.path.append('../../utils')
        from motor_driver_class import motor_driver
        motor = motor_driver()
        print("Initialized Motors")

    encoder = encoder_class()
    
    _ = input("Press enter to start right encoder testing --- ")
    
    print("Right Counter Test")
    encoder.init_counter()
    if (run_motor > 0):
        motor.forward()
    encoder.count_till(20, encoder.read_right)
    if (run_motor > 0):
        motor.gameover()
        
    _ = input("Press enter to continue left encoder testing --- ")
    
    print("Left Counter Test")
    encoder.init_counter()
    if (run_motor > 0):
        motor.forward()
    encoder.count_till(20, encoder.read_left)
    if (run_motor > 0):
        motor.gameover()
    
    if (run_motor > 0):
        motor.cleanup()
    encoder.cleanup()