import time

import sys
sys.path.append('../../utils')

from imu_thread_class import imu_thread
from motor_driver_class import motor_driver

motor = motor_driver()
motor.init_pwm_mode()
print("motors set to pwm opereation")

imu = imu_thread()
imu.start_read()
print("IMU inititalized and started to read")

init_angle = imu.get_orientation()[0]
final_angle  = (init_angle + 90)/360

motor.pwm_drive("pivotright", 80)
while 1:
    angle = imu.get_orientation()
    print(f'init angle = {init_angle[0]} :: angle = {angle[0]}')
    if(angle < final_angle+2 and angle > final_angle-2):
        break
    time.sleep(0.1)
motor.pwm_drive("stop")

motor.cleanup()
imu.cleanup()