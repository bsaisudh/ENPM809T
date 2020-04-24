import RPi.GPIO as gpio
import time
import numpy as np

class encoder_class:
    def __init__(self):
        self.init_counter()
        self.init()
        self.callbackR = None
        self.callbackL = None
        self.paramsR = None
        self.paramsL = None
        
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
    
    def init_counter(self): # union is useful here since only two counters will be used at a time
        self.counter = np.uint(0)
        self.counterR = np.uint(0)
        self.counterL = np.uint(0)
        
    def init_callback(self, fntnptrR, _paramsR, fntnptrL, _paramsL):
        self.callbackL = fntnptrL
        self.callbackR = fntnptrR
        self.paramsL = _paramsL
        self.paramsR = _paramsR
    
    def count_till(self, count, read_fntn, data = None):
        self.init_counter()
        button = int(0)
        while True:
            reading = read_fntn()
            if data != None:
                data.append(reading)
            if(int(reading) != button):
                button = reading
                self.counter += 1
                print(f"Counter Value : {self.counter}")
            if self.counter >= count:
                print ("--- Thanks for playing the game ---")
                break
        return data
    
    def countRL_till(self, countR, countL, dataR = None, dataL = None):
        self.init_counter()
        buttonR = int(0)
        buttonL = int(0)
        while True:
            readingL = self.read_left()
            readingR = self.read_right()
            if dataR != None:
                dataR.append(readingR)
                dataL.append(readingL)
            
            if(int(readingL) != buttonL):
                buttonL = readingL
                self.counterL += 1
                print(f"R : {self.counterR} -- L : {self.counterL}")
            if(int(readingR) != buttonR):
                buttonR = readingR
                self.counterR += 1
                print(f"R : {self.counterR} -- L : {self.counterL}")
                
            if self.counterR >= countR:
                if self.callbackR != None:
                    self.callbackR(*self.paramsR)
            if self.counterL >= countL:
                if self.callbackL != None:
                    self.callbackL(*self.paramsL)
                    
            if self.counterR >= countR and self.counterL >= countL:
                print ("--- Thanks for playing the game ---")
                break
        
        return dataR, dataL
    
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