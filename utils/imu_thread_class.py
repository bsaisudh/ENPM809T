from threading import Thread, Event
from queue import Queue

import time
import string
import socket, traceback

class imu_thread:
    def __init__(self, host_id = "192.168.0.23", port_num = 5555):
        self.q = Queue(maxsize = 1)
        self.exit_event = Event()
        self.host = host_id
        self.port = port_num
        self.s = None
        self.imu_thread = None
        self.init_socket()
    
    def init_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.s.bind((self.host, self.port))
    
    def cleanup(self):
        if self.imu_thread is not None:
            self.stop_read()
    
    @staticmethod  
    def read_imu(socket_s, que:Queue, exit_evnt:Event):
        # t = time.time()
        while 1:
            message, address = socket_s.recvfrom(8192)
            message = message.decode("utf-8")
            message = message.strip(" 'b ")
            message = message.split(',')
            # print(time.time() - t)
            # t = time.time()
            try:
                ndx = message.index(' 81')
                orientation = message[ndx+1:ndx+4]
                orientation = [float(x) for x in orientation]
                # print(orientation)
                que.put(orientation)
            except ValueError:
                pass
            if exit_evnt.is_set():
                print("IMU Thread Stopped")
                break
        
    def start_read(self):
        self.imu_thread = Thread(target = imu_thread.read_imu,
                                 args = (self.s,
                                         self.q,
                                         self.exit_event,))
        self.imu_thread.start()
    
    def stop_read(self):
        self.exit_event.set()
        print('exit_event_set, waiting for join')
        self.imu_thread.join()
        print('Thread Joined')
        self.imu_thread = None
        print('Thread stopped')
        
    def get_orientation(self):
        return self.q.get()

if __name__ == "__main__":
    print("test")
    imu = imu_thread()
    imu.start_read()
    for i in range(20):
        print(f'--> {i} : {imu.q.get()}')
    imu.stop_read()
    imu.cleanup()