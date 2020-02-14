\## import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the Raspberry Pi camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(640,480))
# allow the camera to warmup
time.sleep(0.1)

# define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
# out = cv2.VideoWriter(‘videoname.avi’, fourcc, 10, (640, 480))
out = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc(*"XVID"), 15, (640,480))
# keep looping
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
	# grab the current frame
	image = frame.array
	# show the frame to our screen
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# write frame to video file
	out.write(image)
	# press the 'q' key to stop the video stream
	if key == ord("q"):
		break

out.release()
camera.close()
