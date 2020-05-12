from process_block import process_block
from process_block import block_calibration

import sys
sys.path.append('../../utils')
from video_recorder import RasPiCamera

camera = RasPiCamera()
block = process_block()
img = camera.capture()

calib = block_calibration()
calib.get_f(camera)

camera.cleanup()
