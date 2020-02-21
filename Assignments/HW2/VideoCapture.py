## import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the Raspberry Pi camera
camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(1280,720))
# allow the camera to warmup
time.sleep(0.1)

# define the codec and create VideoWriter object
# fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
# out = cv2.VideoWriter(‘videoname.avi’, fourcc, 10, (640, 480))
out = cv2.VideoWriter('video.avi',cv2.VideoWriter_fourcc(*"XVID"), 2, (1280,720))
# keep looping
start = time.time()
video_start_time = time.time()
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=False):
	# grab the current frame
	image = frame.array
	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)
	# show the frame to our screen
	image = cv2.flip(image, -1)
	cv2.imshow("Frame", image)
	key = cv2.waitKey(1) & 0xFF
	# write frame to video file
	out.write(image)
	# press the 'q' key to stop the video stream
	if key == ord("q"):
		break
	print(f'--> {time.time()-start} ; {time.time()-video_start_time} ')
	if time.time() - video_start_time > 40:
		break
	start = time.time()

out.release()
camera.close()
