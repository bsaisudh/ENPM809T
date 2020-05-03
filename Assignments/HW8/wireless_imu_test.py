'''
Message Example
b'620901.02908, 3,   0.242,  0.606,  9.527, 4,   0.020, -0.006,  0.001, 5, -24.762,-223.451,-98.491, 81, 173.805, -3.304,  1.315'
'''

import time
import string
import socket, traceback

host="192.168.0.23"
port=5555
s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
s.bind((host, port))
temp1=0
prev_time = time.time()
while 1:
    while 0:
        start = time.time()
        message, address = s.recvfrom(8192)
        print(message)
        print(address)
        end = time.time()
        print(f'{end - start}')
    while 1:
        message, address = s.recvfrom(8192)
        print(f'{len(message)}')
        # print(message)
        # print(address)
        message = message.decode("utf-8")
        message = message.strip(" 'b ")
        message = message.split(',')
        try:
            ndx = message.index(' 81')
            orientation = message[ndx+1:ndx+4]
            orientation = [float(x) for x in orientation]
            if(time.time() - prev_time > 0.0):
                print(f"{time.time() - prev_time} -- orientation : {orientation}")
                prev_time = time.time()
            break
        except ValueError:
            # print("no data")
            pass
    time.sleep(0.5)
    