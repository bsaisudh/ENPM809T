import RPi.GPIO as gpio
import time

from servo_class import Servo

s = Servo()
for i in range(10, 20):
    print(f"duty cycle : {i/2}")
    s.set_dutycycle(i/2)
    time.sleep(1)
    
for i in range(20, 9, -1):
    print(f"duty cycle : {i/2}")
    s.set_dutycycle(i/2)
    time.sleep(1)
    
s.cleanup()


