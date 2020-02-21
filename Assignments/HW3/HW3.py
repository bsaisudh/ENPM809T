## import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

# initialize the Raspberry Pi camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

# define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
# out = cv2.VideoWriter(‘videoname.avi’, fourcc, 10, (1280, 720))
out = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc(*"XVID"), 2, (640, 480))

# initialize  timing metrics variables
start = time.time()
video_start_time = time.time()
proc_time = []

# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
	# grab the current frame
	image = frame.array
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# show the frame to our screen
	image = cv2.flip(image, -1)
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	# -------- Code for green detection here ---------
	#
	#
	# ---------------------

	# write frame to video file
	out.write(image)
	# press the 'q' key to stop the video stream
	if key == ord("q"):
		break
	# calculate process time for each frame
	proc_time.append(time.time()-start)
	print(f'--> Current frame process time - {proc_time[-1]} S ; Total Time - {proc_time[-1]-video_start_time} S')
	if time.time() - video_start_time > 40:
		break
	start = time.time()

# cleanup - close camera and close video writer
out.release()
camera.close()

# metrics
# save to text file
np.savetxt('hw3data.txt', proc_time, delimiter = ',')
# plot processing time
plt.figure()
plt.plot(list(range(len(proc_time))), proc_time)
plt.show()
# plot histogram
plt.figure()
plt.hist(proc_time, 20)
plt.show()
