import RPi.GPIO as gpio
import time

class servo_class:
    def __init__(self):
        self.init_servo()
        self.pwm = None
        self.init_pwm()
        
    def init_servo(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(36, gpio.OUT) #servo signal sw PWM
        
    def init_pwm(self):
        self.pwm = gpio.PWM(36, 50)
        self.pwm.start(5)
    
    def cleanup(self):
        self.set_dutycycle(5)
        time.sleep(1)
        self.pwm.stop()
        gpio.cleanup()
        
    def set_dutycycle(self, dc, check = True):
        if (not(check) or (dc >= 5 and dc <= 10)):
            self.pwm.ChangeDutyCycle(dc)
        else:
            print("**ERROR** : duty cycle out of range [0,10]")
        
    def release_load(self):
        self.set_dutycycle(0, check = False)
            
if __name__ == "__main__" :
    s = Servo()
    while(True):
        try:
            dc = float(input("Duty Cycle: "))
            if dc == 0 :
                print("release load")
                s.release_load()
            elif dc > 0 :
                s.set_dutycycle(dc)
            else:
                break
        except:
            break
    print("closing pwm")
    s.cleanup()
        
    
            
        
        
    
    
