import RPi.GPIO as gpio
import time

class motor_driver:
    def __init__(self):
        self.init()
    
    def init(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(31, gpio.OUT) #IN1
        gpio.setup(33, gpio.OUT) #IN2
        gpio.setup(35, gpio.OUT) #IN3
        gpio.setup(37, gpio.OUT) #IN4

    def cleanup(self):
        gpio.cleanup()
    
    def gameover(self):
        # Set all pins LOW
        gpio.output(31, False)
        gpio.output(33, False)
        gpio.output(35, False)
        gpio.output(37, False)


    def forward(self, tf = 0):
        # Left wheels
        gpio.output(31, True)
        gpio.output(33, False)
        # Right wheels
        gpio.output(35, False)
        gpio.output(37, True)
        
        # Wait
        if tf > 0 :
            time.sleep(tf)
            # Set all pins low and cleanup
            self.gameover()

    def reverse(self, tf = 0):
        # Left wheels
        gpio.output(31, False)
        gpio.output(33, True)
        # Right wheels
        gpio.output(35, True)
        gpio.output(37, False)
        # Wait
        if tf > 0:
            time.sleep(tf)
            # Set all pins low and cleanup
            self.gameover()


    def pivotright(self, tf = 0):
        # Left wheels
        gpio.output(31, True)
        gpio.output(33, False)
        # Right wheels
        gpio.output(35, True)
        gpio.output(37, False)
        # Wait
        if tf > 0:
            time.sleep(tf)
            # Set all pins low and cleanup
            self.gameover()

    def pivotleft(self, tf = 0):
        # Left wheels
        gpio.output(31, False)
        gpio.output(33, True)
        # Right wheels
        gpio.output(35, False)
        gpio.output(37, True)
        # Wait
        if tf > 0:
            time.sleep(tf)
            # Set all pins low and cleanup
            self.gameover()

    def key_input(self, event, tf = 0):
        print("Key: ", event)
        key_press = event
        
        if key_press.lower() == 'w':
            self.forward(tf)
        elif key_press.lower() == 's':
            self.reverse(tf)
        elif key_press.lower() == 'a':
            self.pivotleft(tf)
        elif key_press.lower() == 'd':
            self.pivotright(tf)
        else:
            print("Invalid key !")

if __name__ == '__main__':
    motor = motor_driver()
    while True:
        key_press = input("Select driving mode: ")
        if key_press == 'q':
            break
        motor.key_input(key_press, 1)
    motor.cleanup()