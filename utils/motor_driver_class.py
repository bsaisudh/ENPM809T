import RPi.GPIO as gpio
import time

class motor_driver:
    def __init__(self):
        self.init()
        self.pwm = None
        self.pwm_mode = False
    
    def init(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(31, gpio.OUT) #IN1
        gpio.setup(33, gpio.OUT) #IN2
        gpio.setup(35, gpio.OUT) #IN3
        gpio.setup(37, gpio.OUT) #IN4
        
    def init_pwm_mode(self):
        self.pwm_mode = True
        self.pwm = []
        for i in [31, 33, 35, 37]:
            self.pwm.append(gpio.PWM(i, 50))
        for i in self.pwm:
            i.start(0)
            
    def cleanup(self):
        if self.pwm_mode:
            self.pwm_gameover()
            for p in self.pwm:
                p.stop()
        self.gameover()
        gpio.cleanup()
        
    
    def set_dutycycle(self, duty_cycles):
        for p, dc in zip(self.pwm, duty_cycles):
            p.ChangeDutyCycle(dc)
            
    def pwm_gameover(self):
        self.set_dutycycle([0, 0, 0, 0])
        
    def pwm_drive(self, direc, dc, tf = 0):
        if direc == "forward":
            self.set_dutycycle([dc, 0, 0, dc])
        if direc == "reverse":
            self.set_dutycycle([0, dc, dc, 0])
        if direc == "pivotright":
            self.set_dutycycle([dc, 0, dc, 0])
        if direc == "pivotleft":
            self.set_dutycycle([0, dc, 0, dc])
        if direc == "stop":
            self.pwm_gameover()
        if tf > 0:
            time.sleep(tf)
            self.pwm_gameover()
        
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