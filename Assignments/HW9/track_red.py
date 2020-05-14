import cv2

from process_block import process_block
from process_block import block_calibration

import sys
sys.path.append('../../utils')
from video_recorder import RasPiCamera

focal_length = 514.2857142857143
obj_hieght = 7
obj_width = 4.1

camera = RasPiCamera()
calib = block_calibration(focal_length, obj_hieght, obj_width)
block = process_block(calib)
img = camera.capture()

# calib.get_f(camera)

while 1:
    img, hieght, center= block.center_hieght(camera.capture())
    dist, angle = block.predict_dist_angle(img.shape)
    if hieght is not None :
        print("-------------")
        print(f'Distance = {dist}, Angle = {angle}')
        print(f'h =  {hieght}, c = {center}, ::{img.shape}::{img.shape[1]/2 - center[0]}')
    cv2.imshow("thres", img)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
cv2.destroyWindow('thres')
cv2.destroyAllWindows()
camera.cleanup()
