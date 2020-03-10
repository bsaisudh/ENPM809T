import RPi.GPIO as gpio

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(31, gpio.OUT) #IN1
    gpio.setup(33, gpio.OUT) #IN1
    gpio.setup(35, gpio.OUT) #IN1
    gpio.setup(37, gpio.OUT) #IN1

def motors_shut_down():
    # Set all pins LOW
    gpio.output(31, False)
    gpio.output(33, False)
    gpio.output(35, False)
    gpio.output(37, False)

if __name__ == '__main__':
    init()
    motors_shut_down()