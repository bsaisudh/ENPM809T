import RPi.GPIO as gpio
import time
import imutils

class sonar_class:
    def __init__(self):
        self.trig = 16
        self.echo = 18
        self.init()
        
    def init(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.trig, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)
        
    def cleanup(self):
        gpio.cleanup()
        
    def measure_distance(self):
        gpio.output(self.trig, False)
        time.sleep(0.1)

        gpio.output(self.trig, True)
        time.sleep(0.000010)
        gpio.output(self.trig, False)

        while gpio.input(self.echo) == 0:
            ps = time.time()

        while gpio.input(self.echo) == 1:
            pe = time.time()

        pd = pe - ps
        dist = pd*17150
        dist = round(dist, 2)
        
        return dist # dist in cm
    
    def measure_dist_avg(self, measurements = 10, disp = False):
        dist = 0
        for i in range(measurements):
            d = self.measure_distance()
            dist += d
            if disp:
                print(f"distance ({i}) : {d}")
        return dist/measurements

if __name__ == "__main__":
    sonar = sonar_class()
    print("--> Distance = {} cm".format(sonar.measure_distance()))
    print("--> Distance = {} cm".format(sonar.measure_dist_avg(20, True)))
    sonar.cleanup()
