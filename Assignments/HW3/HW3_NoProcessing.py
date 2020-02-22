## import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

# custom imports
from traffic_light_detection import threshold_hsv_green

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
frame_num = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
	# grab the current frame
	image = frame.array
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	proc_time.append(time.time()-start)
	print(f'--> Frame {frame_num} process time - {proc_time[-1]} S ; Total Time - {proc_time[-1]-video_start_time} S')
	if frame_num > 105:
		break
	start = time.time()
	frame_num +=1

# cleanup - close camera and close video writer
out.release()
camera.close()

# metrics
# save to text file
np.savetxt('hw3data.txt', proc_time, delimiter = ',')
# plot processing time
plt.figure()
plt.plot(list(range(len(proc_time))), proc_time, label='Raw Data')
plt.xlabel('Frame')
plt.ylabel('Processing Time (sec)')
plt.title('Processing Time')
plt.legend()
plt.show()
# plot histogram
plt.figure()
plt.hist(proc_time, 20)
plt.xlabel('Precessing Time (sec)')
plt.ylabel('Number of frames')
plt.title('Processing Time')
plt.show()
