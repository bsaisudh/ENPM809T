import time

class controller_util:
    def __init__(self):
        pass
    
    def set_sp(self, _sp):
        pass
    
    def exec_fntn(self, control):
        pass
    
    def error_fntn(self):
        return 0
    
    def game_over(self):
        pass

class pid_controller:
    def __init__(self, _util:controller_util, _kp = 1, _ki = 1, _kd = 1):
        self.kp = _kp
        self.ki = _ki
        self.kd = _kd
        self.util = _util
        
        
    def controller(self, dev, dt = 0.1):
        i_e = 0
        e = 0
        d_e = 0
        prev_e = 0
        control = 0
        while 1:
            e = self.util.error_fntn()
            i_e += e
            d_e = (prev_e - e)*dt
            prev_e = e
            control = self.kp*e + self.kd*d_e + self.ki*i_e
            self.util.exec_fntn(control)
            time.sleep(dt)
            print(f'c : {control:.2f} - e : {e:.2f} - ie : {i_e:.2f} : de : {d_e:.2f} :: {self.kp*e:.2f} : {self.kd*d_e:.2f} : {self.ki*i_e:.2f}')
            if abs(e) < dev:
                break
        self.util.game_over()
        print('game over PID')