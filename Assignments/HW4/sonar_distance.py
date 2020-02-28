import RPi.GPIO as gpio
import time
import numpy as np
import cv2
import imutils
import os

trig = 16
echo = 18

def distance():
    gpio.setmode(gpio.BOARD)
    gpio.setup(trig, gpio.OUT)
    gpio.setup(echo, gpio.IN)

    gpio.output(trig, False)
    time.sleep(0.1)

    gpio.output(trig, True)
    time.sleep(0.000010)
    gpio.output(trig, False)

    while gpio.input(echo) == 0:
        ps = time.time()

    while gpio.input(echo) == 1:
        pe = time.time()

    pd = pe - ps
    dist = pd*17150
    dist = round(dist, 2)

    gpio.cleanup()
    return dist

if __name__ == "__main__":
    print("--> Distance = {} cm".format(distance()))
    t_dist = 0
    for i in range(10):
        d = distance()
        print(f"--> loop {i} Distance : {d} cm")
        t_dist = t_dist + d
    avg_dist = t_dist/10
    avg_dist_str = f"--> Avg Dist= {avg_dist:.2f} cm"
    print(avg_dist_str)

    name = "sonar_check.jpg"
    os.system('raspistill -w 640 -h 480 -o ' + name)

    img = cv2.imread('sonar_check.jpg')
    img = cv2.flip(img, -1)
    img = cv2.putText(img, avg_dist_str, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.imshow("Sonar Check", img)
    cv2.waitKey(0)
    
    cv2.imwrite("sonar_check.jpg", img)
