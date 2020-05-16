import time

import sys
sys.path.append('../../utils')

from imu_thread_class import imu_thread
from motor_driver_class import motor_driver
from pid_controller_class import pid_controller, controller_util

class turn_right_util(controller_util):
    def __init__(self, _motor:motor_driver, _imu:imu_thread):
        self.motor = _motor
        self.imu = _imu
        self.sp = None
        self.error = None
        
    def set_sp(self, _sp):
        self.sp = _sp
        self.error = None
    
    def game_over(self):
        self.motor.pwm_drive("stop")
        
    def error_fntn(self):
        current_value = self.imu.get_orientation()[0]
        self.error = self.sp - current_value
        print(f'err = {self.sp} - {current_value} = {self.error}')
        return self.error
    
    def exec_fntn(self, control):
        control =  max(min(100, control), -100)
        if self.error >= 0:
            self.motor.pwm_drive("pivotright", int(abs(control)))
        else:
            self.motor.pwm_drive("pivotleft", int(abs(control)))
        
if __name__ == "__main__" :  
    motor = motor_driver()
    motor.init_pwm_mode()
    print("motors set to pwm opereation")

    imu = imu_thread()
    imu.start_read()
    print("IMU inititalized and started to read")

    util_rt_turn = turn_right_util(motor, imu)
    pid_rt = pid_controller(util_rt_turn, 0.5, 0.005, 0.000001)

    init_angle = imu.get_orientation()
    print(f" --> {init_angle[0] + 90} ::: {init_angle[0]}")
    util_rt_turn.set_sp(init_angle[0] + 90)
    pid_rt.controller(2.0)

    print("PID Done")

    motor.cleanup()
    imu.stop_read()
    imu.cleanup()
