import RPi.GPIO as gpio
import time

class motor_driver:
    def __init__(self, tf = 1):
        self.init()
        self.exec_time = tf # in seconds
    
    def init(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(31, gpio.OUT) #IN1
        gpio.setup(33, gpio.OUT) #IN1
        gpio.setup(35, gpio.OUT) #IN1
        gpio.setup(37, gpio.OUT) #IN1

    def cleanup(self):
        gpio.cleanup()
    
    def gameover(self):
        # Set all pins LOW
        gpio.output(31, False)
        gpio.output(33, False)
        gpio.output(35, False)
        gpio.output(37, False)


    def forward(self):
        # Left wheels
        gpio.output(31, True)
        gpio.output(33, False)
        # Right wheels
        gpio.output(35, False)
        gpio.output(37, True)
        # Wait
        time.sleep(self.exec_time)
        # Set all pins low and cleanup
        self.gameover()

    def reverse(self):
        # Left wheels
        gpio.output(31, False)
        gpio.output(33, True)
        # Right wheels
        gpio.output(35, True)
        gpio.output(37, False)
        # Wait
        time.sleep(self.exec_time)
        # Set all pins low and cleanup
        self.gameover()


    def pivotright(self):
        # Left wheels
        gpio.output(31, True)
        gpio.output(33, False)
        # Right wheels
        gpio.output(35, True)
        gpio.output(37, False)
        # Wait
        time.sleep(self.exec_time)
        # Set all pins low and cleanup
        self.gameover()

    def pivotleft(self):
        # Left wheels
        gpio.output(31, False)
        gpio.output(33, True)
        # Right wheels
        gpio.output(35, False)
        gpio.output(37, True)
        # Wait
        time.sleep(self.exec_time)
        # Set all pins low and cleanup
        self.gameover()

    def key_input(self, event):
        print("Key: ", event)
        key_press = event
        
        if key_press.lower() == 'w':
            self.forward()
        elif key_press.lower() == 's':
            self.reverse()
        elif key_press.lower() == 'a':
            self.pivotleft()
        elif key_press.lower() == 'd':
            self.pivotright()
        else:
            print("Invalid key !")

if __name__ == '__main__':
    motor = motor_driver(1)
    motor.exec_time = 1
    while True:
        key_press = input("Select driving mode: ")
        if key_press == 'q':
            break
        motor.key_input(key_press)
    motor.cleanup()